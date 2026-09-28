#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 1.1 (1. Hafta 1. Ödev)
KONU  : Bir Klasördeki Tüm Resimleri 1024x768 Boyutuna Ölçekleme
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Belirtilen girdi klasöründeki tüm görselleri tarar.
 2. Her görseli cv2.resize ve INTER_AREA enterpolasyonu kullanarak 1024x768 boyutuna getirir.
 3. Çıktıları çıktı klasörüne kaydeder ve süre ile boyut bilgilerini raporlar.
"""

import argparse
import time
from pathlib import Path
import cv2

HEDEF_GENISLIK = 1024
HEDEF_YUKSEKLIK = 768
RESIM_UZANTILARI = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def olcekle(resim):
    """
    OpenCV resize fonksiyonu (GENİŞLİK, YÜKSEKLİK) sıralaması bekler.
    Küçültme işlemlerinde piksel aliasing'i önlemek için en uygun interpolasyon cv2.INTER_AREA'dır.
    """
    return cv2.resize(resim, (HEDEF_GENISLIK, HEDEF_YUKSEKLIK), interpolation=cv2.INTER_AREA)


def main():
    parser = argparse.ArgumentParser(description="Klasördeki resimleri 1024x768 boyutuna ölçekle.")
    parser.add_argument("girdi", nargs="?", type=Path, default=Path(__file__).parent / "girdi")
    parser.add_argument("cikti", nargs="?", type=Path, default=Path(__file__).parent / "cikti")
    args = parser.parse_args()

    args.cikti.mkdir(parents=True, exist_ok=True)
    dosyalar = sorted(p for p in args.girdi.iterdir() if p.suffix.lower() in RESIM_UZANTILARI)
    if not dosyalar:
        raise SystemExit(f"Hata: {args.girdi} içinde desteklenen resim dosyası bulunamadı.")

    print(f"[+] {len(dosyalar)} adet resim ölçekleniyor (Hedef: {HEDEF_GENISLIK}x{HEDEF_YUKSEKLIK})...")
    baslangic = time.perf_counter()

    log_lines = []
    for yol in dosyalar:
        resim = cv2.imread(str(yol))
        if resim is None:
            print(f"  [!] ATLANDI (Okunamadı): {yol.name}")
            continue

        yeni = olcekle(resim)
        hedef_yol = args.cikti / yol.name
        cv2.imwrite(str(hedef_yol), yeni)

        bilgi = f"{yol.name:15s}: {resim.shape[1]}x{resim.shape[0]} -> {yeni.shape[1]}x{yeni.shape[0]}"
        print(f"  * {bilgi}")
        log_lines.append(bilgi)

    gecen_sure = time.perf_counter() - baslangic
    ozet = f"\nTamamlandı: {len(dosyalar)} dosya, {gecen_sure:.4f} saniye."
    print(ozet)
    log_lines.append(ozet)

    with open(args.cikti / "resize_cikti.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))


if __name__ == "__main__":
    main()
