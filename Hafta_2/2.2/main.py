#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 2.2 (2. Hafta 2. Ödev)
KONU  : Görüntüyü 4 Parçaya Bölüp Thread'ler ile İşleme ve Süre Kıyaslaması
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Gri görüntüyü 4 eşit kadrana (sol üst, sağ üst, sol alt, sağ alt) böler.
 2. Her parçaya farklı bir piksel dönüşümü uygular:
    - 1. Parça (Sol Üst) : Parlaklığı artır (x + 50)
    - 2. Parça (Sağ Üst): Parlaklığı azalt (x - 50)
    - 3. Parça (Sol Alt) : Negatifini al (255 - x)
    - 4. Parça (Sağ Alt): Gamma 0.5 dönüşümü (sqrt(x/255) * 255)
 3. Bu işlemi hem sıralı (1 thread) hem de paralel (4 thread) olarak 20 kez tekrarlayıp
    ortalama süreleri kıyaslar ve cikti/parca_sonuc.png olarak birleştirip kaydeder.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter
import cv2
import numpy as np


def bol_dort_parca(gri: np.ndarray):
    """Görüntüyü 4 eşit kadrana böler ve dilimleme indisleriyle döndürür."""
    h, w = gri.shape
    mid_y, mid_x = h // 2, w // 2
    return [
        (gri[:mid_y, :mid_x], (slice(0, mid_y), slice(0, mid_x))),
        (gri[:mid_y, mid_x:], (slice(0, mid_y), slice(mid_x, w))),
        (gri[mid_y:, :mid_x], (slice(mid_y, h), slice(0, mid_x))),
        (gri[mid_y:, mid_x:], (slice(mid_y, h), slice(mid_x, w)))
    ]


def isle_parca(girdi):
    """Her parça için belirlenen dönüşümü uygular."""
    sira, parca = girdi
    x = parca.astype(np.float32)
    if sira == 0:
        x += 50.0                  # Parlaklık artır
    elif sira == 1:
        x -= 50.0                  # Parlaklık azalt
    elif sira == 2:
        x = 255.0 - x              # Negatif
    else:
        x = np.sqrt(x / 255.0) * 255.0  # Gamma 0.5 (Aydınlatma)
    return np.clip(x, 0, 255).astype(np.uint8)


def parcalari_isle(gri: np.ndarray, paralel: bool = True) -> np.ndarray:
    bolumler = bol_dort_parca(gri)
    girdiler = [(i, parca) for i, (parca, _) in enumerate(bolumler)]

    if paralel:
        with ThreadPoolExecutor(max_workers=4) as havuz:
            sonuclar = list(havuz.map(isle_parca, girdiler))
    else:
        sonuclar = [isle_parca(g) for g in girdiler]

    birlesik = np.empty_like(gri)
    for (_, dilim), islenmis in zip(bolumler, sonuclar):
        birlesik[dilim] = islenmis
    return birlesik


def sure_olc(gri: np.ndarray, paralel: bool, tekrar: int = 20):
    baslangic = perf_counter()
    sonuc = None
    for _ in range(tekrar):
        sonuc = parcalari_isle(gri, paralel)
    ortalama_sure = (perf_counter() - baslangic) / tekrar
    return ortalama_sure, sonuc


def main():
    parser = argparse.ArgumentParser(description="4 Parça x 4 Thread Parlaklık İşlemi")
    parser.add_argument("girdi", nargs="?", type=Path, default=Path(__file__).parent / "dama.jpg")
    parser.add_argument("cikti", nargs="?", type=Path, default=Path(__file__).parent / "cikti")
    parser.add_argument("--tekrar", type=int, default=20)
    args = parser.parse_args()

    gri = cv2.imread(str(args.girdi), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise SystemExit(f"Görüntü okunamadı: {args.girdi}")

    tek_sure, _ = sure_olc(gri, False, args.tekrar)
    dort_sure, sonuc = sure_olc(gri, True, args.tekrar)

    args.cikti.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.cikti / "parca_sonuc.png"), sonuc)

    rapor = (
        f"Ödev 2.2 Dört Parça Paralel İşleme Raporu ({args.tekrar} Tekrar Ortalaması):\n"
        f"  * 1 Thread (Sıralı İşlem) Süresi: {tek_sure:.6f} saniye\n"
        f"  * 4 Thread (Paralel İşlem) Süresi: {dort_sure:.6f} saniye\n"
        f"  * Hızlanma (Speedup): {tek_sure / dort_sure:.2f}x\n"
        f"  * Çıktı Görseli: parca_sonuc.png başarıyla oluşturuldu.\n"
    )
    print(rapor)
    with open(args.cikti / "parca_thread_cikti.txt", "w", encoding="utf-8") as f:
        f.write(rapor)


if __name__ == "__main__":
    main()
