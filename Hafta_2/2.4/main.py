#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 2.4 (2. Hafta 4. Ödev)
KONU  : Histogram Hesaplama Sürelerini (1 Thread vs 4 Thread) Ölçme ve Kıyaslama
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 1 thread ile tüm görüntünün histogramını hesaplar.
 2. 4 thread ile 4 parçanın histogramını hesaplayıp toplar.
 3. Her iki yöntemi 20 tekrar ile ölçerek ortalama süreleri ve farkı raporlar.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter
import cv2
import numpy as np


def tum_histogram(gri: np.ndarray) -> np.ndarray:
    return np.bincount(gri.ravel(), minlength=256)


def bol_dort(gri: np.ndarray):
    h, w = gri.shape
    mid_y, mid_x = h // 2, w // 2
    return [gri[:mid_y, :mid_x], gri[:mid_y, mid_x:], gri[mid_y:, :mid_x], gri[mid_y:, mid_x:]]


def histogram_4_thread(gri: np.ndarray) -> np.ndarray:
    parcalar = bol_dort(gri)
    with ThreadPoolExecutor(max_workers=4) as havuz:
        hists = list(havuz.map(tum_histogram, parcalar))
    return np.sum(hists, axis=0)


def sure_olc(gri: np.ndarray, hesapla_fonk, tekrar: int = 20):
    baslangic = perf_counter()
    sonuc = None
    for _ in range(tekrar):
        sonuc = hesapla_fonk(gri)
    return (perf_counter() - baslangic) / tekrar, sonuc


def main():
    parser = argparse.ArgumentParser(description="Histogram sürelerini karşılaştır.")
    parser.add_argument("girdi", nargs="?", type=Path, default=Path(__file__).parent / "dama.jpg")
    parser.add_argument("cikti", nargs="?", type=Path, default=Path(__file__).parent / "cikti")
    parser.add_argument("--tekrar", type=int, default=20)
    args = parser.parse_args()

    gri = cv2.imread(str(args.girdi), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise SystemExit(f"Görüntü okunamadı: {args.girdi}")

    tek_sure, hist_tek = sure_olc(gri, tum_histogram, args.tekrar)
    dort_sure, hist_dort = sure_olc(gri, histogram_4_thread, args.tekrar)

    assert np.array_equal(hist_tek, hist_dort), "Histogram sonuçları eşit değil!"

    args.cikti.mkdir(parents=True, exist_ok=True)
    rapor = (
        f"Ödev 2.4 Histogram Süre Kıyaslama Tablosu ({args.tekrar} Tekrar Ortalaması):\n"
        f"--------------------------------------------------------------------\n"
        f"  * 1 Thread (Doğrudan np.bincount) Süresi : {tek_sure:.6f} saniye\n"
        f"  * 4 Thread (Parça + Toplama) Süresi       : {dort_sure:.6f} saniye\n"
        f"  * Süre Farkı (4 Thread - 1 Thread)       : {dort_sure - tek_sure:+.6f} saniye\n"
        f"--------------------------------------------------------------------\n"
        f"Değerlendirme: NumPy C çekirdeğinde tek thread bincount zaten oldukça optimize ve hızlıdır.\n"
        f"Thread başlatma maliyeti (overhead) ve parça birleştirme toplama süresi ölçülmüştür.\n"
    )
    print(rapor)
    with open(args.cikti / "histogram_sure_cikti.txt", "w", encoding="utf-8") as f:
        f.write(rapor)


if __name__ == "__main__":
    main()
