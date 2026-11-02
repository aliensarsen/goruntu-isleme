#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 6.3 (6. Hafta 3. Ödev)
KONU  : OpenCV HoughCircles ile Çember Tespiti
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 'smarties.png' görüntüsünde Canny ve 3x3 medyan filtrelemesi uygular.
 2. cv2.HoughCircles (cv2.HOUGH_GRADIENT) fonksiyonu ile şeker çemberlerini tespit eder.
 3. Tespit edilen çemberlerin merkezlerini ve çevrelerini çizip kaydeder.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA6_DIR = KLASOR.parent
GIRDI = HAFTA6_DIR / "girdi" / "smarties.png"
CIKTI = KLASOR / "cikti"

CEMBER_RENGI = (255, 255, 0)  # camgöbeği
MERKEZ_RENGI = (0, 0, 255)    # kırmızı


def main():
    renkli = cv2.imread(str(GIRDI), cv2.IMREAD_COLOR)
    if renkli is None:
        raise FileNotFoundError(f"Resim okunamadı: {GIRDI}")
    CIKTI.mkdir(parents=True, exist_ok=True)

    gri = cv2.cvtColor(renkli, cv2.COLOR_BGR2GRAY)
    kenar = cv2.Canny(gri, 50, 150)
    kenar_median = cv2.medianBlur(kenar, 3)

    cv2.imwrite(str(CIKTI / "kenar_canny.png"), kenar)
    cv2.imwrite(str(CIKTI / "kenar_median.png"), kenar_median)

    # HoughCircles: dp=2, minDist=30, param1=100, param2=20, minRadius=20, maxRadius=40
    cemberler = cv2.HoughCircles(
        kenar_median,
        cv2.HOUGH_GRADIENT,
        dp=2,
        minDist=30,
        param1=100,
        param2=20,
        minRadius=20,
        maxRadius=40
    )

    cizim = renkli.copy()
    sayi = 0
    bilgiler = []

    if cemberler is not None:
        cemberler_int = np.round(cemberler[0]).astype(int)
        for idx, (x, y, r) in enumerate(cemberler_int, 1):
            cv2.circle(cizim, (x, y), r, CEMBER_RENGI, 2)
            cv2.circle(cizim, (x, y), 2, MERKEZ_RENGI, 3)
            bilgiler.append(f"  {idx:2d}. Çember: Merkez=({x:3d}, {y:3d}), Yarıçap={r:2d} px")
        sayi = len(cemberler_int)

    cv2.imwrite(str(CIKTI / "cemberler_houghcircles.png"), cizim)

    rapor = (
        "============================================================\n"
        "Ödev 6.3: OpenCV HoughCircles Çember Tespiti Raporu\n"
        "============================================================\n\n"
        f"Girdi Görüntüsü        : smarties.png ({renkli.shape[1]}x{renkli.shape[0]})\n"
        f"Tespit Edilen Çember Sayısı: {sayi}\n\n"
        "Çember Detayları:\n" + "\n".join(bilgiler) + "\n"
    )

    with open(CIKTI / "rapor.txt", "w", encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print("✓ Ödev 6.3 tamamlandı.")


if __name__ == "__main__":
    main()
