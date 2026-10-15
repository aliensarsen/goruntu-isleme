#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 4.3 (4. Hafta 3. Ödev)
KONU  : 3x3 Sobel Gradyan Operatörü, Büyüklük ve İkili Kenar Haritası
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Girdi kamera görüntüsüne 5x5 Gauss yumuşatma (sigma=1.0) uygular.
 2. 3x3 Sobel operatörü ile gx (dikey kenarlar), gy (yatay kenarlar) ve hypot (büyüklük) hesaplar.
 3. Tepe gradyan değerinin %20'si eşik kabul edilerek ikili (binary) kenar haritası üretir.
 4. 2x3'lük görsel analiz panosu oluşturur ve çıktıları kaydeder.
"""

from pathlib import Path
import sys
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA4_DIR = KLASOR.parent
sys.path.insert(0, str(HAFTA4_DIR))

from kenarlar import (
    gauss_yumusat,
    gradyan_ikili,
    isaretli_goruntu_uint8,
    mutlak_uint8,
    panel_olustur,
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

    # 1. 5x5 Gauss Yumuşatma + Sobel (gx, gy, hypot)
    gx, gy, mag = sobel(gri, yumusat=True)
    gx_vis = isaretli_goruntu_uint8(gx)
    gy_vis = isaretli_goruntu_uint8(gy)
    mag_vis = mutlak_uint8(mag)
    ikili = gradyan_ikili(mag, esik_orani=0.2)

    # 2. Panel: 2x3 Grid
    yumusak = gauss_yumusat(gri)
    panel = panel_olustur(
        [gri, yumusak, gx_vis, gy_vis, mag_vis, ikili],
        [
            "1. Girdi (Orijinal)",
            "2. 5x5 Gauss Yumusatma",
            "3. Sobel Gx (Dikey Kenar)",
            "4. Sobel Gy (Yatay Kenar)",
            "5. Gradyan Buyuklugu (Hypot)",
            "6. Ikili Kenar (Esik %20)",
        ],
        (2, 3),
    )

    # 3. Çıktıları kaydet
    cv2.imwrite(str(cikti_klasor / "kamera_sobel_gx.png"), gx_vis)
    cv2.imwrite(str(cikti_klasor / "kamera_sobel_gy.png"), gy_vis)
    cv2.imwrite(str(cikti_klasor / "kamera_sobel_hypot.png"), mag_vis)
    cv2.imwrite(str(cikti_klasor / "kamera_sobel_ikili.png"), ikili)
    cv2.imwrite(str(cikti_klasor / "panel_sobel.png"), panel)

    print("✓ Ödev 4.3 (Sobel 3x3) başarıyla tamamlandı.")


if __name__ == "__main__":
    main()
