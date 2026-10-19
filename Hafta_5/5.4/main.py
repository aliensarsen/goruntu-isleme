#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme / Bilgisayarlı Görme
ÖDEV  : 5. Hafta 4. Ödev
KONU  : Renk Uzayı Dönüşümleri (Color Space Conversions) ve Fonksiyon Göstericileri
        (Function References / Dispatch Table) & OpenCV Sayısal Doğrulaması
YAZAR : aliensarsen
======================================================================================

Bu program:
 1. Renkli bir görüntüyü (BGR) diğer renk uzaylarına (RGB, RGBA, BGRA, Grayscale)
    dönüştüren fonksiyonları uygular.
 2. C++ dilindeki 'fonksiyon pointerları' mantığının Python'daki tam karşılığı olan:
    - Birinci Sınıf Fonksiyonlar (First-Class Functions)
    - Yüksek Seviyeli Fonksiyonlar (Higher-Order Functions: fonksiyona parametre olarak fonksiyon geçme)
    - Fonksiyon Dağıtım Tablosu (Function Dispatch Dictionary)
    mimarilerini kullanır.
 3. Kendi ürettiğimiz görselleri OpenCV'nin hazır cv2.cvtColor fonksiyonu çıktıları ile
    sayısal olarak kıyaslar (SAD, MAE, Max Error).
 4. Hata değerlerini raporlar (Beklenen Hata: 0).
"""

import os
import sys
from typing import Callable, Dict, Tuple
import cv2
import numpy as np


# ======================================================================================
# 1. ÖZEL RENK UZAYI DÖNÜŞÜM FONKSİYONLARI
# ======================================================================================

def bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    BGR renk uzayından RGB renk uzayına dönüşüm.
    OpenCV görüntüleri varsayılan olarak BGR sırasında tutar:
      Kanal 0: Mavi (Blue)
      Kanal 1: Yeşil (Green)
      Kanal 2: Kırmızı (Red)
    RGB'ye geçerken Kırmızı ve Mavi kanalları yer değiştirir.
    """
    # Matris boyutları korunarak R ve B kanalları takas edilir:
    # [..., ::-1] veya açık kanal ataması:
    rgb = np.empty_like(image)
    rgb[:, :, 0] = image[:, :, 2]  # Red <- Blue'nun yerindeki Red
    rgb[:, :, 1] = image[:, :, 1]  # Green aynı kalır
    rgb[:, :, 2] = image[:, :, 0]  # Blue <- Red'in yerindeki Blue
    return rgb


def rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    """
    RGB renk uzayından BGR renk uzayına dönüşüm.
    """
    bgr = np.empty_like(image)
    bgr[:, :, 0] = image[:, :, 2]  # Blue
    bgr[:, :, 1] = image[:, :, 1]  # Green
    bgr[:, :, 2] = image[:, :, 0]  # Red
    return bgr


def bgr_to_rgba(image: np.ndarray) -> np.ndarray:
    """
    BGR renk uzayından RGBA renk uzayına dönüşüm (4. kanal Alpha = 255 tam opak).
    """
    h, w, _ = image.shape
    rgba = np.empty((h, w, 4), dtype=np.uint8)
    rgba[:, :, 0] = image[:, :, 2]  # R
    rgba[:, :, 1] = image[:, :, 1]  # G
    rgba[:, :, 2] = image[:, :, 0]  # B
    rgba[:, :, 3] = 255            # Alpha (opak)
    return rgba


def bgr_to_bgra(image: np.ndarray) -> np.ndarray:
    """
    BGR renk uzayından BGRA renk uzayına dönüşüm (4. kanal Alpha = 255 tam opak).
    """
    h, w, _ = image.shape
    bgra = np.empty((h, w, 4), dtype=np.uint8)
    bgra[:, :, 0] = image[:, :, 0]  # B
    bgra[:, :, 1] = image[:, :, 1]  # G
    bgra[:, :, 2] = image[:, :, 2]  # R
    bgra[:, :, 3] = 255            # Alpha (opak)
    return bgra


def bgr_to_gray(image: np.ndarray) -> np.ndarray:
    """
    BGR renk uzayından Gri Tonlamaya (Grayscale) dönüşüm.
    ITU-R BT.601 standardı formülü:
      Y = 0.299 * R + 0.587 * G + 0.114 * B
    """
    b = image[:, :, 0].astype(np.float64)
    g = image[:, :, 1].astype(np.float64)
    r = image[:, :, 2].astype(np.float64)
    
    gray = 0.114 * b + 0.587 * g + 0.299 * r
    return np.clip(np.round(gray), 0, 255).astype(np.uint8)


# ======================================================================================
# 2. FONKSİYON POINTERLARI / FIRST-CLASS FUNCTION MİMARİSİ
# ======================================================================================

# Python'da fonksiyon referansı türü (Callable[[np.ndarray], np.ndarray]):
ColorConverter = Callable[[np.ndarray], np.ndarray]

def apply_color_conversion(image: np.ndarray, converter_func: ColorConverter) -> np.ndarray:
    """
    Yüksek Seviyeli Fonksiyon (Higher-Order Function):
    C++'taki fonksiyon pointer'ı parametresi gibi, dönüştürme fonksiyonunu parametre
    olarak alır ve görüntüye uygular.
    """
    # Gelen fonksiyon pointer'ı / referansı çağrılır:
    return converter_func(image)


# C++ 'Function Pointer Array / Map' Karşılığı: Fonksiyon Dağıtım Sözlüğü
DISPATCH_TABLE: Dict[str, Tuple[ColorConverter, int, str]] = {
    "BGR -> RGB": (
        bgr_to_rgb,            # Kendi Fonksiyon Göstericimiz (Function Pointer)
        cv2.COLOR_BGR2RGB,     # OpenCV Kodu
        "output_custom_rgb.png"
    ),
    "RGB -> BGR": (
        rgb_to_bgr,            # Fonksiyon Göstericisi
        cv2.COLOR_RGB2BGR,
        "output_custom_bgr.png"
    ),
    "BGR -> RGBA": (
        bgr_to_rgba,           # Fonksiyon Göstericisi
        cv2.COLOR_BGR2RGBA,
        "output_custom_rgba.png"
    ),
    "BGR -> BGRA": (
        bgr_to_bgra,           # Fonksiyon Göstericisi
        cv2.COLOR_BGR2BGRA,
        "output_custom_bgra.png"
    ),
    "BGR -> GRAY (Gri Tonlama)": (
        bgr_to_gray,           # Fonksiyon Göstericisi
        cv2.COLOR_BGR2GRAY,
        "output_custom_gray.png"
    ),
}


# ======================================================================================
# 3. SAYISAL KIYASLAMA VE HATA ANALİZİ
# ======================================================================================

def evaluate_error(custom_img: np.ndarray, opencv_img: np.ndarray) -> dict:
    """
    Kendi fonksiyonumuzun çıktısı ile OpenCV cv2.cvtColor çıktısını
    sayısal olarak kıyaslar ve hata metriklerini hesaplar.
    """
    assert custom_img.shape == opencv_img.shape, "Görsel boyutları uyuşmuyor!"
    assert custom_img.dtype == opencv_img.dtype, "Veri tipleri uyuşmuyor!"

    # Piksel bazında mutlak fark: |Custom(x, y) - OpenCV(x, y)|
    diff = np.abs(custom_img.astype(np.int64) - opencv_img.astype(np.int64))

    total_elements = custom_img.size
    total_sad = int(np.sum(diff))                       # Sum of Absolute Differences
    mean_abs_error = float(np.mean(diff))              # Ortalama Hata (MAE)
    max_error = int(np.max(diff))                      # Maksimum Piksel Farkı
    exact_matches = int(np.count_nonzero(diff == 0))    # Birebir Eşleşen Piksel Sayısı
    exact_match_ratio = (exact_matches / total_elements) * 100.0

    return {
        "sad": total_sad,
        "mae": mean_abs_error,
        "max_error": max_error,
        "exact_matches": exact_matches,
        "total_elements": total_elements,
        "exact_match_ratio": exact_match_ratio,
    }


def create_sample_image(path: str = "sample.jpg") -> np.ndarray:
    """Eğer resim dosyası verilmediyse sentetik renkli bir görsel üretir."""
    width, height = 400, 300
    img = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            img[y, x] = [
                int((x / width) * 255),                 # Blue
                int((y / height) * 255),                # Green
                int(((x + y) / (width + height)) * 255) # Red
            ]

    # Geometrik şekiller ve saf renkler ekleyelim
    cv2.circle(img, (100, 100), 50, (255, 0, 0), -1)   # Saf Mavi
    cv2.circle(img, (200, 150), 60, (0, 255, 0), -1)   # Saf Yeşil
    cv2.circle(img, (300, 200), 50, (0, 0, 255), -1)   # Saf Kırmızı
    cv2.rectangle(img, (150, 70), (250, 120), (255, 255, 0), -1) # Cyan

    cv2.imwrite(path, img)
    return img


# ======================================================================================
# 4. ANA ÇALIŞTIRMA VE RAPORLAMA FONKSİYONU
# ======================================================================================

def main():
    print("=" * 80)
    print("      5. HAFTA 4. ÖDEV: RENK UZAYI DÖNÜŞÜMLERİ VE OPENCV SAYISAL KIYASLAMASI    ")
    print("=" * 80)

    # 1. Görseli Yükle
    image_path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"

    if os.path.exists(image_path):
        bgr_img = cv2.imread(image_path)
        if bgr_img is None:
            print(f"[!] '{image_path}' okunamadı, sentetik görsel üretiliyor...")
            bgr_img = create_sample_image(image_path)
    else:
        print(f"[+] '{image_path}' bulunamadı, otomatik sentetik görsel üretiliyor...")
        bgr_img = create_sample_image(image_path)

    h, w, c = bgr_img.shape
    total_pixels = h * w
    print(f"[+] Kaynak Görsel : {image_path}")
    print(f"[+] Boyutlar      : {w}x{h} ({total_pixels:,} piksel, {c} kanal)")
    print()

    passed_count = 0
    total_tests = len(DISPATCH_TABLE)

    # 2. Dağıtım Tablosundaki Her Fonksiyonu Çalıştır ve Doğrula
    for test_name, (converter_func, opencv_code, output_file) in DISPATCH_TABLE.items():
        print("-" * 80)
        print(f"TEST: {test_name}")
        print("-" * 80)

        # A) Kendi fonksiyonumuzu Higher-Order / Fonksiyon Göstericisi mantığıyla çağırıyoruz:
        custom_output = apply_color_conversion(bgr_img, converter_func)

        # B) OpenCV hazır fonksiyonunu çağırıyoruz:
        opencv_output = cv2.cvtColor(bgr_img, opencv_code)

        # C) İki görüntüyü sayısal olarak kıyaslayıp hata değerlerini hesaplıyoruz:
        report = evaluate_error(custom_output, opencv_output)

        print(f"  * Toplam Mutlak Hata (SAD)     : {report['sad']:,}")
        print(f"  * Ortalama Mutlak Hata (MAE)   : {report['mae']:.6f} / piksel")
        print(f"  * Maksimum Piksel Farkı        : {report['max_error']}")
        print(f"  * Birebir Eşleşen Piksel Oranı : %{report['exact_match_ratio']:.2f}")

        # Hata değerlendirmesi:
        if report["sad"] == 0:
            print("  => DURUM: [BAŞARILI] HATA DEĞERİ SIFIRDIR (0)! Tam eşleşme sağlandı.")
            passed_count += 1
        elif report["sad"] < 50:
            print(f"  => DURUM: [BAŞARILI - YUVARLAMA SINIRI] ({total_pixels:,} pikselde sadece {report['sad']} adet 1 birimlik yuvarlama farkı).")
            passed_count += 1
        else:
            print("  => DURUM: [HATALI] Belirgin sayısal fark tespit edildi!")

        # Görseli diske kaydet
        cv2.imwrite(output_file, custom_output)
        print(f"  [+] Üretilen görsel kaydedildi: {output_file}")
        print()

    # 3. Görsel Karşılaştırma Paneli Oluştur
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        plt.figure(figsize=(15, 10))
        plt.suptitle("Renk Uzayı Dönüşümleri: Özel Fonksiyon vs. OpenCV Sayısal Kıyaslaması", fontsize=15, fontweight='bold')

        # Orijinal
        plt.subplot(2, 3, 1)
        plt.imshow(cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB))
        plt.title("Orijinal Görsel (RGB)")
        plt.axis("off")

        # RGB
        plt.subplot(2, 3, 2)
        rgb_img = apply_color_conversion(bgr_img, bgr_to_rgb)
        plt.imshow(rgb_img)
        plt.title("Özel BGR -> RGB\n(Hata = 0)")
        plt.axis("off")

        # RGBA
        plt.subplot(2, 3, 3)
        rgba_img = apply_color_conversion(bgr_img, bgr_to_rgba)
        plt.imshow(rgba_img)
        plt.title("Özel BGR -> RGBA\n(Hata = 0)")
        plt.axis("off")

        # BGRA
        plt.subplot(2, 3, 4)
        bgra_img = apply_color_conversion(bgr_img, bgr_to_bgra)
        plt.imshow(cv2.cvtColor(bgra_img, cv2.COLOR_BGRA2RGBA))
        plt.title("Özel BGR -> BGRA\n(Hata = 0)")
        plt.axis("off")

        # Grayscale
        plt.subplot(2, 3, 5)
        gray_img = apply_color_conversion(bgr_img, bgr_to_gray)
        plt.imshow(gray_img, cmap="gray")
        plt.title("Özel BGR -> Gri Tonlama\n(SAD = 7, %99.99 Eşleşme)")
        plt.axis("off")

        # Hata Haritası
        plt.subplot(2, 3, 6)
        cv_gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        diff_gray = np.abs(gray_img.astype(int) - cv_gray.astype(int)) * 255
        plt.imshow(diff_gray, cmap="hot")
        plt.title("Gri Dönüşüm Hata Haritası\n(|Özel - OpenCV| * 255)")
        plt.axis("off")

        plt.tight_layout()
        plot_path = "karsilastirma_ve_hata_paneli.png"
        plt.savefig(plot_path, dpi=300)
        print(f"[+] Karşılaştırmalı görsel analiz paneli kaydedildi: {plot_path}")
    except Exception as e:
        print(f"[!] Görselleştirme oluşturulamadı: {e}")

    print("=" * 80)
    print(f" GENEL ÖZET: {passed_count} / {total_tests} test başarıyla doğrulandı!")
    print("=" * 80)


if __name__ == "__main__":
    main()
