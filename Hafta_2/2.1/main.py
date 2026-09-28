#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 2.1 (2. Hafta 1. Ödev)
KONU  : 8-Bit Gri Görüntüyü 6-Bit Parlaklık Seviyesine Nicemleme (Quantization)
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 8-bit (256 gri tonu: 0-255) formatındaki görüntüyü okur.
 2. Alt 2 biti atıp (nicemleyerek) görüntüyü 6-bit (64 farklı gri seviyesi) derinliğe indirger.
 3. Orijinal ve nicemlenmiş görüntü arasındaki mutlak fark görüntüsünü (amplified difference) üretir.
 4. Çıktıları cikti/ klasörüne kaydeder ve benzersiz seviye sayılarını raporlar.
"""

import argparse
from pathlib import Path
import cv2
import numpy as np


def nicemle_6bit(gri: np.ndarray) -> np.ndarray:
    """
    8-bit [0, 255] piksel değerini 6-bit derinliğe nicemler:
    Alt 2 biti sıfırlayarak (sağa 2 bit, sonra sola 2 bit kaydırarak)
    256 seviyeyi 64 eş aralıklı seviyeye indirir.
    """
    return ((gri >> 2) << 2).astype(np.uint8)


def fark_gorseli(gri: np.ndarray, nicemli: np.ndarray) -> np.ndarray:
    """Orijinal ve nicemli arasındaki farkı görünür kılmak için [0, 255]'e normalize eder."""
    fark = cv2.absdiff(gri, nicemli)
    en_buyuk = int(fark.max())
    if en_buyuk == 0:
        return fark
    return (fark.astype(np.float32) * (255 / en_buyuk)).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(description="8-bit gri görüntüyü 6-bit seviyesine nicemle.")
    parser.add_argument("girdi", nargs="?", type=Path, default=Path(__file__).parent / "dama.jpg")
    parser.add_argument("cikti", nargs="?", type=Path, default=Path(__file__).parent / "cikti")
    args = parser.parse_args()

    gri = cv2.imread(str(args.girdi), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise SystemExit(f"Hata: Görüntü okunamadı: {args.girdi}")

    nicemli = nicemle_6bit(gri)
    fark = fark_gorseli(gri, nicemli)

    args.cikti.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.cikti / "gri.png"), gri)
    cv2.imwrite(str(args.cikti / "6bit.png"), nicemli)
    cv2.imwrite(str(args.cikti / "fark.png"), fark)

    orijinal_seviye = np.unique(gri).size
    nicemli_seviye = np.unique(nicemli).size

    rapor = (
        f"Ödev 2.1 Nicemleme Raporu:\n"
        f"Orijinal Gri Benzersiz Seviye Sayısı: {orijinal_seviye} (Maksimum 256)\n"
        f"6-Bit Nicemli Benzersiz Seviye Sayısı: {nicemli_seviye} (Maksimum 64)\n"
        f"Maksimum Piksel Kuantalama Hatası    : {int(cv2.absdiff(gri, nicemli).max())} seviye (Beklenen <= 3)\n"
    )
    print(rapor)
    with open(args.cikti / "nicemle_6bit_cikti.txt", "w", encoding="utf-8") as f:
        f.write(rapor)


if __name__ == "__main__":
    main()
