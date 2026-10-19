#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme
ÖDEV  : 5.3 (5. Hafta 3. Ödev)
KONU  : Özel Gri Tonlama Dönüşümü ve OpenCV Mutlak Hata Analizi
YAZAR : aliensarsen
======================================================================================
"""

import os
import sys
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def custom_bgr2gray(bgr_image: np.ndarray) -> np.ndarray:
    """
    ITU-R BT.601 standardına göre RGB/BGR -> Gri Tonlama dönüşümü.
    Y = 0.299 * Red + 0.587 * Green + 0.114 * Blue
    """
    blue = bgr_image[:, :, 0].astype(np.float64)
    green = bgr_image[:, :, 1].astype(np.float64)
    red = bgr_image[:, :, 2].astype(np.float64)

    gray = 0.114 * blue + 0.587 * green + 0.299 * red
    return np.clip(np.round(gray), 0, 255).astype(np.uint8)


def create_sample_image(output_path="sample.jpg"):
    """Test için sentetik renkli bir görsel üretir."""
    width, height = 400, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            img[y, x] = [
                int((x / width) * 255),
                int((y / height) * 255),
                int(((x + y) / (width + height)) * 255)
            ]

    cv2.circle(img, (100, 100), 50, (255, 0, 0), -1)
    cv2.circle(img, (200, 150), 60, (0, 255, 0), -1)
    cv2.circle(img, (300, 200), 50, (0, 0, 255), -1)
    cv2.rectangle(img, (150, 70), (250, 120), (255, 255, 0), -1)

    cv2.imwrite(output_path, img)
    return output_path


def main(image_path="sample.jpg"):
    print("=" * 70)
    print(" ÖDEV 5.3: ÖZEL GRİ DÖNÜŞÜM VE OPENCV MUTLAK HATA ANALİZİ")
    print("=" * 70)

    if not os.path.exists(image_path):
        image_path = create_sample_image(image_path)

    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        raise ValueError(f"Görsel açılamadı: {image_path}")

    h, w, c = bgr_img.shape
    total_pixels = h * w
    print(f"[+] Görsel: {image_path} ({w}x{h}, {total_pixels:,} piksel)")
    print()

    # 1. OpenCV hazır fonksiyonu ile griye dönüştürme
    gray_opencv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("output_gray_opencv.jpg", gray_opencv)
    print("[1] OpenCV cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) çalıştırıldı -> output_gray_opencv.jpg")

    # 2. Kendi yazdığımız fonksiyon ile griye dönüştürme
    gray_custom = custom_bgr2gray(bgr_img)
    cv2.imwrite("output_gray_custom.jpg", gray_custom)
    print("[2] Kendi custom_bgr2gray() fonksiyonumuz çalıştırıldı      -> output_gray_custom.jpg")

    # 3. İki görselin eşleşen piksellerinin mutlak farklarının toplamı (Hata Değeri)
    abs_diff = np.abs(gray_opencv.astype(np.int32) - gray_custom.astype(np.int32))
    total_sad = int(np.sum(abs_diff))
    mean_abs_error = float(np.mean(abs_diff))
    max_error = int(np.max(abs_diff))
    exact_matches = int(np.count_nonzero(abs_diff == 0))
    match_percentage = (exact_matches / total_pixels) * 100.0

    print("\n[3] HATA RAPORU (Mutlak Farkların Toplamı):")
    print("-" * 50)
    print(f"  Toplam Mutlak Hata (SAD)     : {total_sad:,}")
    print(f"  Ortalama Mutlak Hata (MAE)   : {mean_abs_error:.6f} piksel")
    print(f"  Maksimum Piksel Farkı        : {max_error}")
    print(f"  Birebir Eşleşen Piksel Oranı : %{match_percentage:.2f} ({exact_matches:,}/{total_pixels:,})")
    print("-" * 50)

    # 4. Görsel Analiz ve Hata Haritası
    fig = plt.figure(figsize=(15, 5))
    fig.suptitle("Ödev 5.3: OpenCV vs. Özel Gri Dönüşüm ve Hata Haritası", fontsize=15, fontweight='bold')

    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB))
    plt.title("Orijinal Renkli")
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.imshow(gray_opencv, cmap="gray")
    plt.title("OpenCV cv2.cvtColor")
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.imshow(gray_custom, cmap="gray")
    plt.title("Özel custom_bgr2gray")
    plt.axis("off")

    plt.subplot(1, 4, 4)
    # Farklar 0 veya 1 olduğundan 255 ile çarparak görselleştiriyoruz
    plt.imshow(abs_diff * 255, cmap="hot")
    plt.title(f"Hata Haritası (|Fark| * 255)\nToplam Hata = {total_sad}")
    plt.axis("off")

    plt.tight_layout()
    plot_path = "gri_donusum_ve_hata_analizi.png"
    plt.savefig(plot_path, dpi=300)
    print(f"\n[+] Karşılaştırma ve hata paneli kaydedildi: {plot_path}")
    print("=" * 70)


if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    main(img_arg)
