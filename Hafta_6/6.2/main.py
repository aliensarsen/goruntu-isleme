#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 6.2 (6. Hafta 2. Ödev)
KONU  : Özel (Sıfırdan) Hough Doğru Dönüşümü ve Oylama Matrisi Analizi
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'sudoku.png' kenar haritası üzerinde standart Hough formülünü sıfırdan hesaplar:
      rho = x * cos(theta) + y * sin(theta)
 2. 2B (rho x theta) oylama (accumulator) matrisini oluşturur ve her kenar pikseli için oy toplar.
 3. Oylama matrisindeki yerel tepe noktalarını (non-maximum suppression mantığıyla) tespit eder.
 4. Oylama matrisinin ısı haritasını (oylama_matrisi.png) ve bulunan doğruları kaydeder.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA6_DIR = KLASOR.parent
GIRDI = HAFTA6_DIR / "girdi" / "sudoku.png"
CIKTI = KLASOR / "cikti"

THETA_ADIM = 180   # 0..179 derece, 1 derecelik adımlarla
ESIK = 100         # bir doğrunun kabul edilmesi için gereken minimum oy


def sin_cos_tablosu(adim: int):
    """Sin ve cos değerleri baştan bir kez hesaplanır ve bellekte tutulur."""
    thetalar = np.arange(adim) * np.pi / adim
    return thetalar, np.cos(thetalar), np.sin(thetalar)


def hough_oylama(kenar: np.ndarray, cos_t: np.ndarray, sin_t: np.ndarray):
    """Oylama matrisi: satır = rho (negatifler için kaydırılmış), sütun = theta."""
    yukseklik, genislik = kenar.shape
    kosegen = int(np.ceil(np.hypot(yukseklik, genislik)))
    oylama = np.zeros((2 * kosegen + 1, len(cos_t)), dtype=np.int32)
    theta_indeks = np.arange(len(cos_t))

    ys, xs = np.nonzero(kenar)
    for x, y in zip(xs, ys):
        rho = np.rint(x * cos_t + y * sin_t).astype(np.int32)
        oylama[rho + kosegen, theta_indeks] += 1
    return oylama, kosegen


def tepeleri_bul(oylama: np.ndarray, esik: int):
    """Eşiği geçen ve 3x3 komşuluğunun en büyüğü olan tepe hücreleri."""
    komsu_max = cv2.dilate(oylama.astype(np.float32), np.ones((3, 3), np.uint8))
    tepe = (oylama >= esik) & (oylama == komsu_max)
    rho_i, theta_i = np.nonzero(tepe)
    sirali = sorted(zip(rho_i, theta_i), key=lambda h: -oylama[h])
    return [(int(r), int(t), int(oylama[r, t])) for r, t in sirali]


def dogru_ciz(resim: np.ndarray, rho: float, cos_v: float, sin_v: float):
    uzunluk = 2 * max(resim.shape)
    x0, y0 = rho * cos_v, rho * sin_v
    p1 = (int(x0 - uzunluk * sin_v), int(y0 + uzunluk * cos_v))
    p2 = (int(x0 + uzunluk * sin_v), int(y0 - uzunluk * cos_v))
    cv2.line(resim, p1, p2, (255, 0, 255), 2)


def oylama_resmi(oylama: np.ndarray) -> np.ndarray:
    """Oylama matrisini görselleştirir."""
    olcekli = (255 * np.sqrt(oylama / max(float(oylama.max()), 1.0))).astype(np.uint8)
    olcekli = cv2.resize(olcekli, (720, olcekli.shape[0]), interpolation=cv2.INTER_NEAREST)
    return cv2.applyColorMap(olcekli, cv2.COLORMAP_INFERNO)


def main():
    renkli = cv2.imread(str(GIRDI), cv2.IMREAD_COLOR)
    if renkli is None:
        raise FileNotFoundError(f"Resim okunamadı: {GIRDI}")
    CIKTI.mkdir(parents=True, exist_ok=True)

    gri = cv2.cvtColor(renkli, cv2.COLOR_BGR2GRAY)
    kenar = cv2.medianBlur(cv2.Canny(gri, 50, 150), 3)

    thetalar, cos_t, sin_t = sin_cos_tablosu(THETA_ADIM)
    oylama, kosegen = hough_oylama(kenar, cos_t, sin_t)
    cv2.imwrite(str(CIKTI / "oylama_matrisi.png"), oylama_resmi(oylama))

    tepeler = tepeleri_bul(oylama, ESIK)
    cizim = renkli.copy()
    rapor_satirlari = [
        "============================================================",
        "Ödev 6.2: Özel Hough Doğru Dönüşümü Analiz Raporu",
        "============================================================",
        f"Oylama Matrisi Boyutu (rho x theta): {oylama.shape}",
        f"Maksimum Oy Sayısı                  : {int(oylama.max())}",
        f"Tespit Edilen Doğru Sayısı (Esik {ESIK}): {len(tepeler)}",
        "",
        "Tespit Edilen Doğrular:"
    ]

    for rho_i, theta_i, oy in tepeler:
        rho = rho_i - kosegen
        deg = float(np.degrees(thetalar[theta_i]))
        dogru_ciz(cizim, rho, cos_t[theta_i], sin_t[theta_i])
        rapor_satirlari.append(f"  * rho={rho:5d} px | theta={deg:5.1f}° | oy={oy} oy")

    cv2.imwrite(str(CIKTI / "dogrular_kendi.png"), cizim)

    with open(CIKTI / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))

    print("\n".join(rapor_satirlari[:10]))
    print(f"... ({len(tepeler)} doğru kaydedildi)")
    print("✓ Ödev 6.2 tamamlandı.")


if __name__ == "__main__":
    main()
