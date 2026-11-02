#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 6.4 (6. Hafta 4. Ödev)
KONU  : Özel (Sıfırdan) 3 Boyutlu Hough Çember Dönüşümü
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'smarties.png' kenar haritası üzerinde 3B parametre uzayında (merkez x, merkez y, yarıçap r)
    çember oylamasını sıfırdan hesaplar:
      a = x - r * cos(theta),  b = y - r * sin(theta)
 2. Aday merkezler için oy / çevre oranını hesaplar ve dinamik eşikleme ile çemberleri seçer.
 3. 3B akümülatörün 2B izdüşüm ısı haritasını (oylama_matrisi_merkezler.png) ve bulunan çemberleri kaydeder.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA6_DIR = KLASOR.parent
GIRDI = HAFTA6_DIR / "girdi" / "smarties.png"
CIKTI = KLASOR / "cikti"

YARICAPLAR = np.arange(20, 41)   # aranan yarıçaplar (20..40 piksel)
ACI_ADIM = 360                   # 1 derecelik adımlarla tam tur
ESIK_ORAN = 0.20                 # oy / çevre >= 0.20 (çevrenin en az %20'si kenar olmalı)
MIN_MERKEZ_UZAKLIGI = 20         # aynı çemberi tekrar seçmemek için minimum mesafe


def sin_cos_tablosu(adim: int):
    thetalar = np.arange(adim) * 2 * np.pi / adim
    return np.cos(thetalar), np.sin(thetalar)


def merkez_kaydirmalari(cos_t: np.ndarray, sin_t: np.ndarray):
    r_izgara = YARICAPLAR[:, None]
    da = np.rint(r_izgara * cos_t).astype(np.int32)
    db = np.rint(r_izgara * sin_t).astype(np.int32)
    r_indeks = np.broadcast_to(np.arange(len(YARICAPLAR))[:, None], da.shape)
    return da.ravel(), db.ravel(), r_indeks.ravel()


def hough_cember_oylama(kenar: np.ndarray, cos_t: np.ndarray, sin_t: np.ndarray) -> np.ndarray:
    """3 boyutlu oylama matrisi: [b (satır), a (sütun), r indeksi]."""
    yukseklik, genislik = kenar.shape
    oylama = np.zeros((yukseklik, genislik, len(YARICAPLAR)), dtype=np.int32)
    da, db, r_indeks = merkez_kaydirmalari(cos_t, sin_t)

    ys, xs = np.nonzero(kenar)
    for x, y in zip(xs, ys):
        a = x - da
        b = y - db
        icerde = (a >= 0) & (a < genislik) & (b >= 0) & (b < yukseklik)
        hucreler = np.unique(np.ravel_multi_index((b[icerde], a[icerde], r_indeks[icerde]), oylama.shape))
        oylama.ravel()[hucreler] += 1
    return oylama


def cemberleri_sec(oylama: np.ndarray):
    """Eşik: oy / (2*pi*r). Güçlüden zayıfa sıralayıp yakın merkezli tekrarları eler."""
    cevre = 2 * np.pi * YARICAPLAR
    oran = oylama / cevre
    b_i, a_i, r_i = np.nonzero(oran >= ESIK_ORAN)
    adaylar = sorted(zip(b_i, a_i, r_i), key=lambda h: -oran[h])

    secilen = []
    for b, a, r in adaylar:
        if all(np.hypot(a - sa, b - sb) >= MIN_MERKEZ_UZAKLIGI for sa, sb, _, _ in secilen):
            secilen.append((int(a), int(b), int(YARICAPLAR[r]), float(oran[b, a, r])))
    return secilen


def oylama_resmi(oylama: np.ndarray) -> np.ndarray:
    """3B matrisin r eksenindeki en büyük oranı: her (a, b) merkezinin en güçlü oyu."""
    oran = (oylama / (2 * np.pi * YARICAPLAR)).max(axis=2)
    olcekli = (255 * np.clip(oran / max(float(oran.max()), 1e-6), 0, 1)).astype(np.uint8)
    return cv2.applyColorMap(olcekli, cv2.COLORMAP_INFERNO)


def main():
    renkli = cv2.imread(str(GIRDI), cv2.IMREAD_COLOR)
    if renkli is None:
        raise FileNotFoundError(f"Resim okunamadı: {GIRDI}")
    CIKTI.mkdir(parents=True, exist_ok=True)

    gri = cv2.cvtColor(renkli, cv2.COLOR_BGR2GRAY)
    kenar = cv2.medianBlur(cv2.Canny(gri, 50, 150), 3)

    cos_t, sin_t = sin_cos_tablosu(ACI_ADIM)
    oylama = hough_cember_oylama(kenar, cos_t, sin_t)
    cv2.imwrite(str(CIKTI / "oylama_matrisi_merkezler.png"), oylama_resmi(oylama))

    cemberler = cemberleri_sec(oylama)
    cizim = renkli.copy()
    bilgiler = []

    for idx, (a, b, r, oran) in enumerate(cemberler, 1):
        cv2.circle(cizim, (a, b), r, (255, 0, 255), 2)
        cv2.circle(cizim, (a, b), 2, (0, 0, 255), 3)
        bilgiler.append(f"  {idx:2d}. Çember: Merkez=({a:3d}, {b:3d}), r={r:2d} px | Oy/Çevre={oran:.2f}")

    cv2.imwrite(str(CIKTI / "cemberler_kendi.png"), cizim)

    rapor = (
        "============================================================\n"
        "Ödev 6.4: Özel 3B Hough Çember Dönüşümü Raporu\n"
        "============================================================\n\n"
        f"Oylama Matrisi Boyutu (b x a x r): {oylama.shape}\n"
        f"Maksimum Oy Sayısı                : {int(oylama.max())}\n"
        f"Eşik (Oy/Çevre >= {ESIK_ORAN}) İle Tespit: {len(cemberler)} çember\n\n"
        "Tespit Edilen Çemberler:\n" + "\n".join(bilgiler) + "\n"
    )

    with open(CIKTI / "rapor.txt", "w", encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print("✓ Ödev 6.4 tamamlandı.")


if __name__ == "__main__":
    main()
