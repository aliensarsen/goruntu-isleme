#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 3.1 (3. Hafta 1. Ödev)
KONU  : Min-Max Doğrusal Kontrast Germe (Linear Contrast Stretching)
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'dag.jpg' ve 'sis.jpg' gri seviyeli görüntülerini okur.
 2. Min-max doğrusal ölçekleme formülüyle piksel değerlerini [0, 255] aralığına gerer:
      y = (x - min) * 255 / (max - min)
 3. İşlemi hem özel fonksiyonla (formülle) hem de OpenCV'nin cv2.normalize fonksiyonuyla uygular.
 4. İki yöntemin çıktısını kıyaslar (Doğrulama: Fark = 0).
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).parent
GIRDI_KLASOR = KLASOR.parent / "girdi"
CIKTI_KLASOR = KLASOR / "cikti"


def kontrast_germe_ozel(gri: np.ndarray) -> np.ndarray:
    en_kucuk = float(gri.min())
    en_buyuk = float(gri.max())
    if en_buyuk == en_kucuk:
        return gri.copy()
    olcekli = (gri.astype(np.float32) - en_kucuk) * 255.0 / (en_buyuk - en_kucuk)
    return np.clip(np.round(olcekli), 0, 255).astype(np.uint8)


def kontrast_germe_opencv(gri: np.ndarray) -> np.ndarray:
    return cv2.normalize(gri, None, 0, 255, cv2.NORM_MINMAX)


def main():
    CIKTI_KLASOR.mkdir(parents=True, exist_ok=True)
    rapor_satirlari = ["Ödev 3.1: Min-Max Doğrusal Kontrast Germe Raporu", "-" * 60]

    for ad in ["dag", "sis"]:
        girdi_yolu = GIRDI_KLASOR / f"{ad}.jpg"
        gri = cv2.imread(str(girdi_yolu), cv2.IMREAD_GRAYSCALE)
        if gri is None:
            print(f"[!] Görsel bulunamadı: {girdi_yolu}")
            continue

        ozel_sonuc = kontrast_germe_ozel(gri)
        cv_sonuc = kontrast_germe_opencv(gri)

        # Karşılaştırma
        fark = np.abs(ozel_sonuc.astype(int) - cv_sonuc.astype(int))
        maks_fark = int(fark.max())
        toplam_sad = int(fark.sum())

        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_ozel.png"), ozel_sonuc)
        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_opencv.png"), cv_sonuc)

        bilgi = (
            f"Görsel: {ad}.jpg\n"
            f"  * Orijinal Aralık : [{int(gri.min())}, {int(gri.max())}]\n"
            f"  * Gerilmiş Aralık : [{int(ozel_sonuc.min())}, {int(ozel_sonuc.max())}]\n"
            f"  * Özel vs. OpenCV : Maksimum Fark = {maks_fark}, Toplam SAD = {toplam_sad} (Tam Eşleşme: {maks_fark == 0})\n"
        )
        print(bilgi)
        rapor_satirlari.append(bilgi)

    with open(CIKTI_KLASOR / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))


if __name__ == "__main__":
    main()
