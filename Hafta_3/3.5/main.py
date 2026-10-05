#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 3.5 (3. Hafta 5. Ödev)
KONU  : 5x5 Medyan Filtresi ile Tuz-Biber Gürültüsü Temizleme ve PSNR Analizi
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'dag_tuz_biber.png' ve 'sis_tuz_biber.png' tuz-biber (salt & pepper) gürültülü görsellerini okur.
 2. 5x5 pencerede 25 komşu pikselin medyanını bulan özel sıralama/medyan algoritmasını uygular.
 3. Kenar pikselleri için cv2.medianBlur ile uyumlu sınır çoğaltma (BORDER_REPLICATE) kullanır.
 4. cv2.medianBlur hazır fonksiyonu ile kıyaslar ve temiz görsellere göre PSNR kazancını hesaplar.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).parent
GIRDI_KLASOR = KLASOR.parent / "girdi"
CIKTI_KLASOR = KLASOR / "cikti"

BOYUT = 5
YARI = BOYUT // 2


def psnr(orijinal: np.ndarray, islenmis: np.ndarray) -> float:
    mse = np.mean((orijinal.astype(np.float64) - islenmis.astype(np.float64)) ** 2)
    if mse == 0:
        return float("inf")
    return float(10 * np.log10(255.0 ** 2 / mse))


def medyan_filtre_ozel(gri: np.ndarray) -> np.ndarray:
    """5x5 medyan filtresini vektörel sıralama katmanları ile uygular."""
    h, w = gri.shape
    # Sınır çoğaltma (cv2.BORDER_REPLICATE mantığı)
    satirlar = [min(max(i, 0), h - 1) for i in range(-YARI, h + YARI)]
    sutunlar = [min(max(j, 0), w - 1) for j in range(-YARI, w + YARI)]
    genis = gri[satirlar][:, sutunlar]

    # 5x5 pencerenin 25 elemanı
    katmanlar = []
    for dy in range(BOYUT):
        for dx in range(BOYUT):
            katmanlar.append(genis[dy:dy + h, dx:dx + w].copy())

    # Vektörize kabarcık/karşılaştırma sıralaması (Tüm pikseller için paralel)
    n = len(katmanlar)
    for tur in range(n - 1):
        for k in range(n - 1 - tur):
            kucuk = np.minimum(katmanlar[k], katmanlar[k + 1])
            buyuk = np.maximum(katmanlar[k], katmanlar[k + 1])
            katmanlar[k], katmanlar[k + 1] = kucuk, buyuk

    # 25 elemanın medyanı 13. elemandır (indeks 12)
    return katmanlar[n // 2]


def medyan_filtre_opencv(gri: np.ndarray) -> np.ndarray:
    return cv2.medianBlur(gri, 5)


def main():
    CIKTI_KLASOR.mkdir(parents=True, exist_ok=True)
    rapor_satirlari = [
        "============================================================",
        "Ödev 3.5: 5x5 Medyan Filtresi ve PSNR Analizi Raporu",
        "============================================================",
        ""
    ]

    for ad in ["dag", "sis"]:
        temiz_yolu = GIRDI_KLASOR / f"{ad}.jpg"
        gurultulu_yolu = GIRDI_KLASOR / f"{ad}_tuz_biber.png"

        temiz = cv2.imread(str(temiz_yolu), cv2.IMREAD_GRAYSCALE)
        gurultulu = cv2.imread(str(gurultulu_yolu), cv2.IMREAD_GRAYSCALE)

        if temiz is None or gurultulu is None:
            print(f"[!] Görseller eksik: {ad}")
            continue

        ozel_sonuc = medyan_filtre_ozel(gurultulu)
        cv_sonuc = medyan_filtre_opencv(gurultulu)

        psnr_gurultulu = psnr(temiz, gurultulu)
        psnr_ozel = psnr(temiz, ozel_sonuc)
        psnr_opencv = psnr(temiz, cv_sonuc)

        fark = np.abs(ozel_sonuc.astype(int) - cv_sonuc.astype(int))
        maks_fark = int(fark.max())
        toplam_sad = int(fark.sum())

        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_ozel.png"), ozel_sonuc)
        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_opencv.png"), cv_sonuc)

        bilgi = (
            f"Görsel: {ad}\n"
            f"  * Tuz-Biber Gürültülü PSNR : {psnr_gurultulu:.2f} dB\n"
            f"  * Özel Medyan Filtreli PSNR: {psnr_ozel:.2f} dB (Kazanç: +{psnr_ozel - psnr_gurultulu:.2f} dB)\n"
            f"  * OpenCV medianBlur PSNR   : {psnr_opencv:.2f} dB\n"
            f"  * Özel vs. OpenCV Fark     : Maks Fark = {maks_fark}, Toplam SAD = {toplam_sad} (Tam Eşleşme: {maks_fark == 0})\n"
        )
        print(bilgi)
        rapor_satirlari.append(bilgi)

    with open(CIKTI_KLASOR / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))


if __name__ == "__main__":
    main()
