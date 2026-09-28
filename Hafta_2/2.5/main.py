#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 2.5 (2. Hafta 5. Ödev)
KONU  : Parlaklık ve Kontrast Dönüşümü (y = 0.75 * x + 20) ve Ayrı Etkileri
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Gri tonlamalı görüntüyü okur.
 2. Şu üç dönüşümü uygular:
    - Sadece Kontrast Azaltma: carp = 0.75 * x
    - Sadece Parlaklık Artırma: topla = x + 20
    - Birlikte Doğrusal Dönüşüm: donusum = 0.75 * x + 20
 3. Dört durumu (Orijinal, carp, topla, donusum) 2x2 ızgara formatında yan yana birleştirip
    cikti/karsilastirma.png olarak kaydeder.
 4. İstatistiki verileri (ortalama, min, max) raporlar.
"""

import argparse
from pathlib import Path
import cv2
import numpy as np


def parlaklik_donusumleri(gri: np.ndarray):
    x = gri.astype(np.float32)
    carp = np.clip(0.75 * x, 0, 255).astype(np.uint8)
    topla = np.clip(x + 20.0, 0, 255).astype(np.uint8)
    birlikte = np.clip(0.75 * x + 20.0, 0, 255).astype(np.uint8)
    return carp, topla, birlikte


def karsilastirma_gorseli(goruntuler):
    etiketler = ("Orijinal", "0.75 * x (Kontrast -)", "x + 20 (Parlaklik +)", "0.75 * x + 20 (Birlikte)")
    hucreler = []
    for img, etiket in zip(goruntuler, etiketler):
        genislik = min(600, img.shape[1])
        yukseklik = max(1, round(img.shape[0] * genislik / img.shape[1]))
        kucuk = cv2.resize(img, (genislik, yukseklik), interpolation=cv2.INTER_AREA)
        hucre = cv2.copyMakeBorder(kucuk, 36, 0, 0, 0, cv2.BORDER_CONSTANT, value=0)
        cv2.putText(hucre, etiket, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255, 1, cv2.LINE_AA)
        hucreler.append(hucre)
    ust = cv2.hconcat(hucreler[:2])
    alt = cv2.hconcat(hucreler[2:])
    return cv2.vconcat([ust, alt])


def main():
    parser = argparse.ArgumentParser(description="Parlaklık dönüşümü y = 0.75*x + 20")
    parser.add_argument("girdi", nargs="?", type=Path, default=Path(__file__).parent / "dama.jpg")
    parser.add_argument("cikti", nargs="?", type=Path, default=Path(__file__).parent / "cikti")
    args = parser.parse_args()

    gri = cv2.imread(str(args.girdi), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise SystemExit(f"Görüntü okunamadı: {args.girdi}")

    carp, topla, birlikte = parlaklik_donusumleri(gri)

    args.cikti.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.cikti / "carp_075.png"), carp)
    cv2.imwrite(str(args.cikti / "topla_20.png"), topla)
    cv2.imwrite(str(args.cikti / "donusum.png"), birlikte)

    karsilastirma = karsilastirma_gorseli((gri, carp, topla, birlikte))
    cv2.imwrite(str(args.cikti / "karsilastirma.png"), karsilastirma)

    rapor = (
        f"Ödev 2.5 Doğrusal Parlaklık / Kontrast Dönüşümü Raporu:\n"
        f"--------------------------------------------------------------------\n"
        f"  * Orijinal Görüntü   : Ortalama = {gri.mean():.2f}, [Min, Max] = [{int(gri.min())}, {int(gri.max())}]\n"
        f"  * 0.75 * x           : Ortalama = {carp.mean():.2f}, [Min, Max] = [{int(carp.min())}, {int(carp.max())}]\n"
        f"  * x + 20             : Ortalama = {topla.mean():.2f}, [Min, Max] = [{int(topla.min())}, {int(topla.max())}]\n"
        f"  * 0.75 * x + 20      : Ortalama = {birlikte.mean():.2f}, [Min, Max] = [{int(birlikte.min())}, {int(birlikte.max())}]\n"
        f"--------------------------------------------------------------------\n"
        f"Sonuç: 0.75 çarpanı kontrastı daraltmış, +20 sabiti ise tüm tonları yukarı ötelemiştir.\n"
    )
    print(rapor)
    with open(args.cikti / "parlaklik_donusum_cikti.txt", "w", encoding="utf-8") as f:
        f.write(rapor)


if __name__ == "__main__":
    main()
