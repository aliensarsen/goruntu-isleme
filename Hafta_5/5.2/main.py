#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme
ÖDEV  : 5.2 (5. Hafta 2. Ödev)
KONU  : Özel calcHist Fonksiyonu Yazma ve Her Kanal İçin Ayrı Ayrı Çalıştırma
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


def custom_calc_hist(channel_matrix: np.ndarray) -> np.ndarray:
    """
    Kendi yazdığımız Histogram Hesaplama Fonksiyonu (cv2.calcHist alternatifi).
    
    Parametre:
        channel_matrix: 2B (Yükseklik x Genişlik) tek kanallı piksel matrisi (0-255).
    Dönüş:
        hist: 256 elemanlı 1B numpy dizisi (her piksel parlaklığının frekansı).
    """
    hist = np.zeros(256, dtype=np.int64)
    flat = channel_matrix.ravel()
    for pixel in flat:
        hist[pixel] += 1
    return hist


def create_sample_image(output_path="sample.jpg"):
    """Test için sentetik renkli bir görsel oluşturur."""
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
    print(" ÖDEV 5.2: ÖZEL calchist FONKSİYONU VE KANAL HİSTOGRAMLARI")
    print("=" * 70)

    if not os.path.exists(image_path):
        image_path = create_sample_image(image_path)

    # 1. Renkli Görüntüyü Oku (OpenCV BGR formatında okur)
    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        raise ValueError(f"Görsel açılamadı: {image_path}")

    h, w, c = bgr_img.shape
    total_pixels = h * w
    print(f"[+] Görsel: {image_path} ({w}x{h}, {total_pixels:,} piksel, {c} kanal)")
    print()

    # 2. Her bir kanal için özel fonksiyonumuzu ayrı ayrı çalıştırma
    channels = [
        {"name": "Mavi (Blue)",   "idx": 0, "color": "blue"},
        {"name": "Yeşil (Green)", "idx": 1, "color": "green"},
        {"name": "Kırmızı (Red)",  "idx": 2, "color": "red"}
    ]

    custom_hists = {}
    cv_hists = {}

    print("[+] Her kanal için 'custom_calc_hist' çalıştırılıyor ve OpenCV ile kıyaslanıyor:")
    for ch in channels:
        idx = ch["idx"]
        name = ch["name"]
        channel_data = bgr_img[:, :, idx]

        # Kendi yazdığımız fonksiyon:
        my_hist = custom_calc_hist(channel_data)
        custom_hists[name] = my_hist

        # OpenCV hazır fonksiyonu (doğrulama için):
        cv_hist = cv2.calcHist([bgr_img], [idx], None, [256], [0, 256]).ravel()
        cv_hists[name] = cv_hist

        # Kıyaslama:
        diff = np.abs(my_hist - cv_hist).sum()
        print(f"  * {name:15s} -> Toplam Piksel: {my_hist.sum():,}, OpenCV ile Mutlak Fark: {diff:.1f}")

    # 3. Görselleştirme Grafiği
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Ödev 5.2: Özel custom_calc_hist Fonksiyonu ile Kanal Histogramları", fontsize=15, fontweight='bold')

    # Subplot 1: Orijinal Görsel
    axes[0, 0].imshow(cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Orijinal Renkli Görsel")
    axes[0, 0].axis("off")

    # Subplot 2: Mavi Kanalı
    axes[0, 1].plot(custom_hists["Mavi (Blue)"], color="blue", linewidth=1.5, label="custom_calc_hist")
    axes[0, 1].set_title("Mavi (Blue) Kanalı Histogramı (Fark = 0.0)")
    axes[0, 1].set_xlabel("Piksel Değeri (0 - 255)")
    axes[0, 1].set_ylabel("Frekans")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)
    axes[0, 1].legend()

    # Subplot 3: Yeşil Kanalı
    axes[1, 0].plot(custom_hists["Yeşil (Green)"], color="green", linewidth=1.5, label="custom_calc_hist")
    axes[1, 0].set_title("Yeşil (Green) Kanalı Histogramı (Fark = 0.0)")
    axes[1, 0].set_xlabel("Piksel Değeri (0 - 255)")
    axes[1, 0].set_ylabel("Frekans")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)
    axes[1, 0].legend()

    # Subplot 4: Kırmızı Kanalı & Tüm Kanallar
    axes[1, 1].plot(custom_hists["Kırmızı (Red)"], color="red", linewidth=1.5, label="Kırmızı")
    axes[1, 1].plot(custom_hists["Mavi (Blue)"], color="blue", linewidth=1.0, alpha=0.6, label="Mavi")
    axes[1, 1].plot(custom_hists["Yeşil (Green)"], color="green", linewidth=1.0, alpha=0.6, label="Yeşil")
    axes[1, 1].set_title("Tüm Kanalların Histogram Dağılımı")
    axes[1, 1].set_xlabel("Piksel Değeri (0 - 255)")
    axes[1, 1].set_ylabel("Frekans")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)
    axes[1, 1].legend()

    plt.tight_layout()
    plot_path = "custom_histogram_grafikleri.png"
    plt.savefig(plot_path, dpi=300)
    print(f"\n[+] Histogram grafiği kaydedildi: {plot_path}")
    print("=" * 70)


if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    main(img_arg)
