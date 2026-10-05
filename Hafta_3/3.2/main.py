#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 3.2 (3. Hafta 2. Ödev)
KONU  : Histogram Eşitleme (Histogram Equalization) - CDF ile Sıfırdan & OpenCV
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 256 seviyeli histogramı hesaplar.
 2. Kümülatif Dağılım Fonksiyonunu (CDF) çıkarır.
 3. CDF'i normalize ederek piksel eşleme tablosunu (LUT) oluşturur:
      T(k) = round( (CDF(k) - CDF_min) / (N - CDF_min) * 255 )
 4. OpenCV cv2.equalizeHist ile kıyaslar ve standart sapma artışını raporlar.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).parent
GIRDI_KLASOR = KLASOR.parent / "girdi"
CIKTI_KLASOR = KLASOR / "cikti"


def histogram_esitleme_ozel(gri: np.ndarray) -> np.ndarray:
    # 1. Histogram
    hist = np.bincount(gri.ravel(), minlength=256)

    # 2. CDF
    cdf = hist.cumsum()

    # 3. Normalizasyon tablosu
    n = gri.size
    cdf_min = cdf[cdf > 0].min()
    tablo = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        if cdf[i] >= cdf_min:
            deger = round((cdf[i] - cdf_min) * 255.0 / (n - cdf_min))
            tablo[i] = max(0, min(255, deger))

    # 4. LUT uygula
    return tablo[gri]


def main():
    CIKTI_KLASOR.mkdir(parents=True, exist_ok=True)
    rapor_satirlari = ["Ödev 3.2: Histogram Eşitleme Raporu", "-" * 60]

    for ad in ["dag", "sis"]:
        girdi_yolu = GIRDI_KLASOR / f"{ad}.jpg"
        gri = cv2.imread(str(girdi_yolu), cv2.IMREAD_GRAYSCALE)
        if gri is None:
            continue

        ozel_sonuc = histogram_esitleme_ozel(gri)
        cv_sonuc = cv2.equalizeHist(gri)

        fark = np.abs(ozel_sonuc.astype(int) - cv_sonuc.astype(int))
        maks_fark = int(fark.max())
        toplam_sad = int(fark.sum())

        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_ozel.png"), ozel_sonuc)
        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_opencv.png"), cv_sonuc)

        bilgi = (
            f"Görsel: {ad}.jpg\n"
            f"  * Orijinal Standart Sapma : {gri.std():.2f}\n"
            f"  * Eşitlenmiş Standart Sapma: {ozel_sonuc.std():.2f}\n"
            f"  * Özel vs. OpenCV Farkı    : Maksimum Fark = {maks_fark}, Toplam SAD = {toplam_sad} (Tam Eşleşme: {maks_fark == 0})\n"
        )
        print(bilgi)
        rapor_satirlari.append(bilgi)

    with open(CIKTI_KLASOR / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))


if __name__ == "__main__":
    main()
