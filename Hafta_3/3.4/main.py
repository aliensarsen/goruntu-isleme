#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 3.4 (3. Hafta 4. Ödev)
KONU  : 3x3 Ortalama (Mean/Box) Filtresi ile Gürültü Temizleme ve PSNR Analizi
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'dag_gurultulu.png' ve 'sis_gurultulu.png' gürültülü görüntülerini okur.
 2. 3x3 ortalama (1/9) çekirdeği ile özel 2D konvolüsyon fonksiyonu uygular.
 3. Kenar pikselleri cv2.blur (BORDER_REFLECT_101 / BORDER_DEFAULT) mantığıyla yansıtılarak ele alınır.
 4. cv2.blur hazır fonksiyonu ile kıyaslar ve orijinal temiz görsellere göre PSNR (dB) hesaplar.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).parent
GIRDI_KLASOR = KLASOR.parent / "girdi"
CIKTI_KLASOR = KLASOR / "cikti"

CEKIRDEK_3X3 = np.ones((3, 3), dtype=np.float64) / 9.0


def psnr(orijinal: np.ndarray, islenmis: np.ndarray) -> float:
    mse = np.mean((orijinal.astype(np.float64) - islenmis.astype(np.float64)) ** 2)
    if mse == 0:
        return float("inf")
    return float(10 * np.log10(255.0 ** 2 / mse))


def ortalama_filtre_ozel(gri: np.ndarray) -> np.ndarray:
    """3x3 Ortalama (Box) filtresini özel konvolüsyonla uygular."""
    h, w = gri.shape
    # Kenar sınırlarını cv2.blur gibi yansıt (BORDER_REFLECT_101: 1 0 1 ... w-2 w-1 w-2)
    satirlar = [1] + list(range(h)) + [h - 2]
    sutunlar = [1] + list(range(w)) + [w - 2]
    genis = gri[satirlar][:, sutunlar].astype(np.float64)

    sonuc = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        ust = genis[y]
        orta = genis[y + 1]
        alt = genis[y + 2]
        satir = sonuc[y]
        for x in range(w):
            toplam = (
                ust[x] * CEKIRDEK_3X3[0, 0] + ust[x + 1] * CEKIRDEK_3X3[0, 1] + ust[x + 2] * CEKIRDEK_3X3[0, 2] +
                orta[x] * CEKIRDEK_3X3[1, 0] + orta[x + 1] * CEKIRDEK_3X3[1, 1] + orta[x + 2] * CEKIRDEK_3X3[1, 2] +
                alt[x] * CEKIRDEK_3X3[2, 0] + alt[x + 1] * CEKIRDEK_3X3[2, 1] + alt[x + 2] * CEKIRDEK_3X3[2, 2]
            )
            satir[x] = int(round(toplam))
    return sonuc


def ortalama_filtre_opencv(gri: np.ndarray) -> np.ndarray:
    return cv2.blur(gri, (3, 3))


def main():
    CIKTI_KLASOR.mkdir(parents=True, exist_ok=True)
    rapor_satirlari = [
        "============================================================",
        "Ödev 3.4: 3x3 Ortalama Filtresi ve PSNR Analizi Raporu",
        "============================================================",
        ""
    ]

    for ad in ["dag", "sis"]:
        temiz_yolu = GIRDI_KLASOR / f"{ad}.jpg"
        gurultulu_yolu = GIRDI_KLASOR / f"{ad}_gurultulu.png"

        temiz = cv2.imread(str(temiz_yolu), cv2.IMREAD_GRAYSCALE)
        gurultulu = cv2.imread(str(gurultulu_yolu), cv2.IMREAD_GRAYSCALE)

        if temiz is None or gurultulu is None:
            print(f"[!] Görseller eksik: {ad}")
            continue

        ozel_sonuc = ortalama_filtre_ozel(gurultulu)
        cv_sonuc = ortalama_filtre_opencv(gurultulu)

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
            f"  * Gürültülü Görüntü PSNR : {psnr_gurultulu:.2f} dB\n"
            f"  * Özel Filtreli PSNR    : {psnr_ozel:.2f} dB (Kazanç: +{psnr_ozel - psnr_gurultulu:.2f} dB)\n"
            f"  * OpenCV Blur PSNR      : {psnr_opencv:.2f} dB\n"
            f"  * Özel vs. OpenCV Fark  : Maks Fark = {maks_fark}, Toplam SAD = {toplam_sad} (Tam Eşleşme: {maks_fark == 0})\n"
        )
        print(bilgi)
        rapor_satirlari.append(bilgi)

    with open(CIKTI_KLASOR / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))


if __name__ == "__main__":
    main()
