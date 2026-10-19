#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme
ÖDEV  : 5.1 (5. Hafta 1. Ödev)
KONU  : Renkli Görüntü Kanal Histogramları ve Siyah-Beyaz Dönüşümü
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


def create_sample_image(output_path="sample.jpg"):
    """Test için sentetik renkli bir görüntü üretir."""
    width, height = 400, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            img[y, x] = [
                int((x / width) * 255),                 # Blue
                int((y / height) * 255),                # Green
                int(((x + y) / (width + height)) * 255) # Red
            ]

    cv2.circle(img, (100, 100), 50, (255, 0, 0), -1)   # Mavi
    cv2.circle(img, (200, 150), 60, (0, 255, 0), -1)   # Yeşil
    cv2.circle(img, (300, 200), 50, (0, 0, 255), -1)   # Kırmızı
    cv2.rectangle(img, (150, 70), (250, 120), (255, 255, 0), -1) # Cyan

    cv2.imwrite(output_path, img)
    return output_path


def main(image_path="sample.jpg"):
    print("=" * 70)
    print(" ÖDEV 5.1: RENKLİ GÖRÜNTÜ KANAL HİSTOGRAMLARI VE SİYAH-BEYAZ DÖNÜŞÜMÜ")
    print("=" * 70)

    if not os.path.exists(image_path):
        image_path = create_sample_image(image_path)

    # 1. Renkli Görüntüyü Oku
    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        raise ValueError(f"Görsel açılamadı: {image_path}")

    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

    # 2. Siyah-Beyaza Dönüştürme
    # A) Gri Tonlama (Grayscale: 0-255 arası gri tonları)
    gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

    # B) Sabit Eşikleme ile İkili Siyah-Beyaz (Threshold = 127)
    _, binary_fixed = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

    # C) Otsu Algoritması ile Otomatik Eşiklenmiş İkili Siyah-Beyaz
    otsu_thresh, binary_otsu = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imwrite("output_grayscale.jpg", gray_img)
    cv2.imwrite("output_binary_fixed.jpg", binary_fixed)
    cv2.imwrite("output_binary_otsu.jpg", binary_otsu)

    print(f"[+] Gri tonlama görseli kaydedildi: output_grayscale.jpg")
    print(f"[+] Sabit eşikleme (127) ikili görsel: output_binary_fixed.jpg")
    print(f"[+] Otsu ikili görseli (Eşik={otsu_thresh:.0f}): output_binary_otsu.jpg")

    # 3. Her Bir Kanal İçin Histogram Çıkarma
    colors = ('b', 'g', 'r')
    channel_names = ('Mavi (Blue)', 'Yeşil (Green)', 'Kırmızı (Red)')

    fig = plt.figure(figsize=(15, 10))
    fig.suptitle("Ödev 5.1: Renk Kanalları Histogramı ve Siyah-Beyaz Dönüşümü", fontsize=15, fontweight='bold')

    plt.subplot(2, 3, 1)
    plt.imshow(rgb_img)
    plt.title("Orijinal Renkli Görüntü (RGB)")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.imshow(gray_img, cmap="gray")
    plt.title("Gri Tonlama (Grayscale)")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.imshow(binary_otsu, cmap="gray")
    plt.title(f"Siyah-Beyaz (Otsu Binary, Eşik={otsu_thresh:.0f})")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    for i, col in enumerate(colors):
        hist = cv2.calcHist([bgr_img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col, linewidth=1.8, label=channel_names[i])
    plt.title("Her Bir Renk Kanalının Histogramı")
    plt.xlabel("Piksel Değeri (0 - 255)")
    plt.ylabel("Piksel Sayısı")
    plt.xlim([0, 256])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.subplot(2, 3, 5)
    hist_gray = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    plt.plot(hist_gray, color='black', linewidth=1.8, label="Gri Ton")
    plt.axvline(x=otsu_thresh, color='red', linestyle='--', label=f'Otsu Eşiği ({otsu_thresh:.0f})')
    plt.title("Gri Seviye Histogramı ve Eşik Değeri")
    plt.xlabel("Piksel Değeri (0 - 255)")
    plt.ylabel("Piksel Sayısı")
    plt.xlim([0, 256])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.subplot(2, 3, 6)
    for i, col in enumerate(colors):
        hist = cv2.calcHist([bgr_img], [i], None, [256], [0, 256])
        plt.fill_between(range(256), hist.ravel(), alpha=0.25, color=col, label=channel_names[i])
    plt.title("Renk Kanalları Yoğunluk Alanı")
    plt.xlabel("Piksel Değeri (0 - 255)")
    plt.ylabel("Piksel Sayısı")
    plt.xlim([0, 256])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.tight_layout()
    result_plot = "histogram_analiz_sonucu.png"
    plt.savefig(result_plot, dpi=300)
    print(f"[+] Analiz paneli kaydedildi: {result_plot}")
    print("=" * 70)


if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    main(img_arg)
