#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 6.5 (6. Hafta 5. Ödev)
KONU  : Gradyan Yönlü Oylama ile Özel Eş Merkezli Çember Tespiti
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'es_merkezli.png' görüntüsünde Gauss ve Canny kenar tespiti yapar.
 2. Sobel gradyan açısını (kenar normalini) hesaplar.
 3. Her kenar pikseli, tüm açılara değil, yalnızca kendi gradyan doğrultusundaki merkezlere oy verir.
 4. Aynı merkeze sahip eş merkezli halkalar akümülatörün aynı (a, b) sütununda birden fazla tepe yapar.
 5. Eş merkezli kümeleri renklendirir ve raporlar.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA6_DIR = KLASOR.parent
GIRDI = HAFTA6_DIR / "girdi" / "es_merkezli.png"
CIKTI = KLASOR / "cikti"

YARICAPLAR = np.arange(10, 111)  # aranan yarıçaplar (10..110 piksel)
ACI_ADIM = 360                   # gradyan açısı 1 derecelik adımla
ACI_PENCERE = 2                  # gradyan açısı toleransı (+-2 derece)
HALKA_ESIK = 0.3                 # bir halka için oy / çevre >= 0.3
HALKA_ARALIGI = 6                # ardışık iki halka arasındaki asgari yarıçap farkı
MIN_HALKA = 2                    # eş merkezli sayılmak için en az 2 halka
MIN_MERKEZ_UZAKLIGI = 15

RENKLER = [(255, 0, 255), (0, 200, 0), (0, 165, 255), (255, 255, 0)]


def sin_cos_tablosu(adim: int):
    thetalar = np.arange(adim) * 2 * np.pi / adim
    return np.cos(thetalar), np.sin(thetalar)


def gradyan_aci_indeksi(gri: np.ndarray) -> np.ndarray:
    gx = cv2.Sobel(gri, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gri, cv2.CV_32F, 0, 1, ksize=3)
    aci = np.arctan2(gy, gx)
    return np.rint(aci / (2 * np.pi) * ACI_ADIM).astype(np.int32) % ACI_ADIM


def es_merkezli_oylama(kenar: np.ndarray, aci_indeksi: np.ndarray,
                       cos_t: np.ndarray, sin_t: np.ndarray) -> np.ndarray:
    yukseklik, genislik = kenar.shape
    oylama = np.zeros((yukseklik, genislik, len(YARICAPLAR)), dtype=np.int32)
    pencere = np.arange(-ACI_PENCERE, ACI_PENCERE + 1)
    r_indeks = np.arange(len(YARICAPLAR))

    ys, xs = np.nonzero(kenar)
    for x, y in zip(xs, ys):
        acilar = (aci_indeksi[y, x] + pencere) % ACI_ADIM
        yon_cos = np.concatenate([cos_t[acilar], -cos_t[acilar]])
        yon_sin = np.concatenate([sin_t[acilar], -sin_t[acilar]])
        a = np.rint(x - YARICAPLAR[:, None] * yon_cos).astype(np.int32)
        b = np.rint(y - YARICAPLAR[:, None] * yon_sin).astype(np.int32)
        r = np.broadcast_to(r_indeks[:, None], a.shape)
        icerde = (a >= 0) & (a < genislik) & (b >= 0) & (b < yukseklik)
        hucreler = np.unique(np.ravel_multi_index((b[icerde], a[icerde], r[icerde]), oylama.shape))
        oylama.ravel()[hucreler] += 1
    return oylama


def sutun_halkalari(oran_sutunu: np.ndarray):
    halkalar = []
    for i in np.argsort(-oran_sutunu):
        if oran_sutunu[i] < HALKA_ESIK:
            break
        if all(abs(i - j) >= HALKA_ARALIGI for j in halkalar):
            halkalar.append(int(i))
    return sorted(halkalar)


def merkezleri_bul(oylama: np.ndarray):
    oran = oylama / (2 * np.pi * YARICAPLAR)
    skor = np.where(oran >= HALKA_ESIK, oran, 0).sum(axis=2)
    b_i, a_i = np.nonzero(skor >= HALKA_ESIK)
    adaylar = sorted(zip(b_i, a_i), key=lambda h: -skor[h])

    secilen = []
    for b, a in adaylar:
        if any(np.hypot(a - sa, b - sb) < MIN_MERKEZ_UZAKLIGI for sa, sb, _, _ in secilen):
            continue
        halkalar = sutun_halkalari(oran[b, a])
        if halkalar:
            secilen.append((int(a), int(b), [int(YARICAPLAR[i]) for i in halkalar], float(skor[b, a])))
    return secilen


def merkez_skoru_resmi(oylama: np.ndarray) -> np.ndarray:
    toplam = (oylama / (2 * np.pi * YARICAPLAR)).sum(axis=2)
    olcekli = (255 * np.sqrt(toplam / max(float(toplam.max()), 1e-6))).astype(np.uint8)
    return cv2.applyColorMap(olcekli, cv2.COLORMAP_INFERNO)


def main():
    renkli = cv2.imread(str(GIRDI), cv2.IMREAD_COLOR)
    if renkli is None:
        raise FileNotFoundError(f"Resim okunamadı: {GIRDI}")
    CIKTI.mkdir(parents=True, exist_ok=True)

    gri = cv2.GaussianBlur(cv2.cvtColor(renkli, cv2.COLOR_BGR2GRAY), (5, 5), 1.2)
    kenar = cv2.Canny(gri, 30, 90)
    cv2.imwrite(str(CIKTI / "kenar_canny.png"), kenar)

    cos_t, sin_t = sin_cos_tablosu(ACI_ADIM)
    oylama = es_merkezli_oylama(kenar, gradyan_aci_indeksi(gri), cos_t, sin_t)
    cv2.imwrite(str(CIKTI / "oylama_merkez_skoru.png"), merkez_skoru_resmi(oylama))

    merkezler = merkezleri_bul(oylama)
    kumeler = [m for m in merkezler if len(m[2]) >= MIN_HALKA]
    tekler = [m for m in merkezler if len(m[2]) < MIN_HALKA]

    cizim = renkli.copy()
    for a, b, yaricaplar, _ in tekler:
        cv2.circle(cizim, (a, b), yaricaplar[0], (128, 128, 128), 1)

    for k, (a, b, yaricaplar, _) in enumerate(kumeler):
        renk = RENKLER[k % len(RENKLER)]
        for r in yaricaplar:
            cv2.circle(cizim, (a, b), r, renk, 2)
        cv2.circle(cizim, (a, b), 3, renk, -1)

    cv2.imwrite(str(CIKTI / "cemberler_es_merkezli.png"), cizim)

    rapor_satirlari = [
        "============================================================",
        "Ödev 6.5: Gradyan Yönlü Eş Merkezli Çember Tespiti Raporu",
        "============================================================",
        f"Görüntü Boyutu                      : {renkli.shape[1]}x{renkli.shape[0]}",
        f"Oylama Matrisi Boyutu (b x a x r)   : {oylama.shape}",
        f"Maksimum Oy                         : {int(oylama.max())}",
        f"Tespit Edilen Eş Merkezli Küme Sayısı: {len(kumeler)}",
        ""
    ]

    for idx, (a, b, yaricaplar, skor) in enumerate(kumeler, 1):
        rapor_satirlari.append(
            f"Küme {idx}: Merkez=({a:3d}, {b:3d}) | Halka Sayısı={len(yaricaplar)} | "
            f"Yarıçaplar={yaricaplar} | Skor={skor:.2f}"
        )

    rapor_satirlari.append(f"\nTek Halkalı (Bağımsız) Merkez Sayısı: {len(tekler)}")

    with open(CIKTI / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))

    print("\n".join(rapor_satirlari))
    print("✓ Ödev 6.5 tamamlandı.")


if __name__ == "__main__":
    main()
