#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 4.4 (4. Hafta 4. Ödev)
KONU  : Prewitt ve Sobel Gradyan Operatörlerinin Karşılaştırmalı Analizi
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Girdi kamera görüntüsünde Prewitt ve Sobel gradyanlarını hesaplar.
 2. Büyüklük haritaları (hypot) ve %20 dinamik eşikli ikili kenar haritalarını çıkarır.
 3. İki yöntem arasındaki fark haritasını hesaplar.
 4. Karşılaştırma paneli (karsilastirma_prewitt_sobel.png) ve sayısal analiz raporunu kaydeder.
"""

from pathlib import Path
import sys
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA4_DIR = KLASOR.parent
sys.path.insert(0, str(HAFTA4_DIR))

from kenarlar import (
    gradyan_ikili,
    mutlak_uint8,
    panel_olustur,
    prewitt,
    sobel,
)


def main():
    cikti_klasor = KLASOR / "cikti"
    cikti_klasor.mkdir(parents=True, exist_ok=True)

    girdi_yol = HAFTA4_DIR / "girdi" / "kamera.png"
    if not girdi_yol.exists():
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {girdi_yol}")

    gri = cv2.imread(str(girdi_yol), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise ValueError("kamera.png okunamadı!")

    # 1. Prewitt ve Sobel (Gauss yumuşatmalı)
    p_gx, p_gy, p_mag = prewitt(gri, yumusat=True)
    p_mag_vis = mutlak_uint8(p_mag)
    p_ikili = gradyan_ikili(p_mag, esik_orani=0.2)

    s_gx, s_gy, s_mag = sobel(gri, yumusat=True)
    s_mag_vis = mutlak_uint8(s_mag)
    s_ikili = gradyan_ikili(s_mag, esik_orani=0.2)

    # 2. Fark Haritası
    fark_mag = np.abs(p_mag_vis.astype(np.int16) - s_mag_vis.astype(np.int16)).astype(np.uint8)
    fark_ikili = cv2.bitwise_xor(p_ikili, s_ikili)

    # 3. Karşılaştırma Panosu (2x3 Grid)
    panel = panel_olustur(
        [gri, p_mag_vis, s_mag_vis, fark_mag, p_ikili, s_ikili],
        [
            "1. Girdi (Orijinal)",
            "2. Prewitt Buyukluk",
            "3. Sobel Buyukluk",
            "4. Buyukluk Farki (|P - S|)",
            "5. Prewitt Ikili Kenar (%20)",
            "6. Sobel Ikili Kenar (%20)",
        ],
        (2, 3),
    )

    cv2.imwrite(str(cikti_klasor / "karsilastirma_prewitt_sobel.png"), panel)
    cv2.imwrite(str(cikti_klasor / "prewitt_ikili.png"), p_ikili)
    cv2.imwrite(str(cikti_klasor / "sobel_ikili.png"), s_ikili)
    cv2.imwrite(str(cikti_klasor / "fark_buyukluk.png"), fark_mag)

    # Sayısal analiz
    p_kenar_sayisi = int(np.count_nonzero(p_ikili))
    s_kenar_sayisi = int(np.count_nonzero(s_ikili))
    ortak_kenar = int(np.count_nonzero(p_ikili & s_ikili))
    iou = ortak_kenar / float(np.count_nonzero(p_ikili | s_ikili))

    rapor = (
        "============================================================\n"
        "Ödev 4.4: Prewitt vs Sobel Karşılaştırma Raporu\n"
        "============================================================\n\n"
        f"Görüntü Boyutu         : {gri.shape[1]}x{gri.shape[0]}\n"
        f"Prewitt Kenar Pikseli  : {p_kenar_sayisi}\n"
        f"Sobel Kenar Pikseli    : {s_kenar_sayisi}\n"
        f"Ortak Kenar Pikseli    : {ortak_kenar}\n"
        f"İkili Benzerlik (IoU)  : {iou:.4f} (%{iou*100:.2f})\n"
        f"Maksimum Büyüklük Farkı: {int(fark_mag.max())}\n"
        f"Ortalama Büyüklük Farkı: {float(fark_mag.mean()):.2f}\n"
    )

    with open(cikti_klasor / "rapor.txt", "w", encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print("✓ Ödev 4.4 tamamlandı.")


if __name__ == "__main__":
    main()
