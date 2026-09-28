#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 2.3 (2. Hafta 3. Ödev)
KONU  : Dört Parçanın Histogramını Thread ile Hesaplayıp Birleştirme
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Görüntüyü 4 eşit kadrana böler.
 2. 4 thread kullanarak her parçanın 256 seviyeli histogramını bağımsız olarak hesaplar.
 3. Parça histogramlarını toplayarak ana görüntü histogramını elde eder.
 4. Bütün görüntünün doğrudan hesaplanan histogramı ile parça toplamını karşılaştırır (Doğrulama: Fark = 0).
 5. Histogram grafiğini oluşturup cikti/histogram.png olarak kaydeder.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import cv2
import numpy as np


def hesapla_histogram(gri: np.ndarray) -> np.ndarray:
    """0-255 aralığındaki piksel sayılarını hesaplar."""
    return np.bincount(gri.ravel(), minlength=256)


def bol_dort(gri: np.ndarray):
    h, w = gri.shape
    mid_y, mid_x = h // 2, w // 2
    return [
        gri[:mid_y, :mid_x],
        gri[:mid_y, mid_x:],
        gri[mid_y:, :mid_x],
        gri[mid_y:, mid_x:]
    ]


def parca_histogramlari(gri: np.ndarray, paralel: bool = True):
    parcalar = bol_dort(gri)
    if paralel:
        with ThreadPoolExecutor(max_workers=4) as havuz:
            return list(havuz.map(hesapla_histogram, parcalar))
    return [hesapla_histogram(p) for p in parcalar]


def histogram_ciz(histogram: np.ndarray) -> np.ndarray:
    """OpenCV ile temiz bir histogram grafiği matrisi üretir."""
    h, w = 400, 512
    grafik = np.zeros((h, w), dtype=np.uint8)
    olcekli = cv2.normalize(histogram.astype(np.float32), None, 0, h - 35, cv2.NORM_MINMAX).ravel()

    for i, val in enumerate(olcekli):
        cv2.line(grafik, (i * 2, h - 1), (i * 2, h - 1 - int(val)), 255, 1)

    cv2.putText(grafik, "Gri Seviye Histogrami (4 Parca Birlestirildi)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, 255, 1)
    cv2.putText(grafik, "0", (4, h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 180, 1)
    cv2.putText(grafik, "255", (w - 40, h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 180, 1)
    return grafik


def main():
    parser = argparse.ArgumentParser(description="Parça histogramlarını paralel hesapla ve birleştir.")
    parser.add_argument("girdi", nargs="?", type=Path, default=Path(__file__).parent / "dama.jpg")
    parser.add_argument("cikti", nargs="?", type=Path, default=Path(__file__).parent / "cikti")
    args = parser.parse_args()

    gri = cv2.imread(str(args.girdi), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise SystemExit(f"Görüntü okunamadı: {args.girdi}")

    # Parça histogramları
    parcalar = parca_histogramlari(gri, paralel=True)
    birlesik_hist = np.sum(parcalar, axis=0)

    # Tam görüntü histogramı
    tam_hist = hesapla_histogram(gri)

    # Doğrulama
    esit_mi = np.array_equal(birlesik_hist, tam_hist)
    assert esit_mi, "Hata: Parça toplamı ile tam görüntü histogramı uyuşmuyor!"

    args.cikti.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.cikti / "histogram.png"), histogram_ciz(birlesik_hist))

    rapor = (
        f"Ödev 2.3 Histogram Birleştirme Doğrulama Raporu:\n"
        f"  * Toplam İşlenen Piksel Sayısı: {int(birlesik_hist.sum()):,} piksel\n"
        f"  * Parça Histogramı Toplamı == Tüm Görüntü Histogramı: {esit_mi} (Fark = 0)\n"
        f"  * Çıktı: cikti/histogram.png başarıyla kaydedildi.\n"
    )
    print(rapor)
    with open(args.cikti / "histogram_thread_cikti.txt", "w", encoding="utf-8") as f:
        f.write(rapor)


if __name__ == "__main__":
    main()
