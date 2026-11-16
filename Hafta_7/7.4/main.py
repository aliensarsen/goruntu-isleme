#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ödev 7.3: Renkli BMP Görüntüsünü Farklı Renk Uzaylarına (HSV, HSI, YUV, CIE Lab) Dönüştürme ve BMP Kaydetme
Ders: Görüntü İşleme
Tarih: 16 Kasım 2026

Bu betik:
1. RGB/BGR renk uzayında ve BMP formatındaki renkli görüntüyü OpenCV ile açar.
2. 4 farklı renk uzayına dönüştürür:
   - HSV: cv2.cvtColor (COLOR_BGR2HSV)
   - HSI: Gonzalez & Woods standart formülüyle sıfırdan vektörize dönüşüm (OpenCV'de doğrudan BGR2HSI yoktur)
   - YUV: cv2.cvtColor (COLOR_BGR2YUV)
   - CIE L*a*b*: cv2.cvtColor (COLOR_BGR2LAB)
3. Her bir renk uzayı sonucunu 3-kanallı 24-bit .bmp formatında kaydeder.
4. Kanalların (H, S, V, I, Y, U, V, L*, a*, b*) istatistiklerini, formüllerini ve karşılaştırmalı görsel panelini üretir.
"""

import os
import sys
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt


def bgr_to_hsi(bgr_img):
    """
    Gonzalez & Woods (Digital Image Processing) standart HSI dönüşümü.
    Girdi: uint8 [0, 255] BGR görüntü
    Çıktı: uint8 [0, 255] HSI görüntü (Kanal 0: H, Kanal 1: S, Kanal 2: I)
    
    Formüller:
    - I = (R + G + B) / 3
    - S = 1 - (3 / (R + G + B)) * min(R, G, B) = 1 - min(R, G, B) / I  (I > 0)
    - theta = arccos( 0.5 * [(R - G) + (R - B)] / sqrt((R - G)^2 + (R - B)(G - B)) )
    - H = theta (B <= G ise) veya 360 - theta (B > G ise)
    """
    bgr_norm = bgr_img.astype(np.float32) / 255.0
    b = bgr_norm[:, :, 0]
    g = bgr_norm[:, :, 1]
    r = bgr_norm[:, :, 2]

    # 1. Intensity (I) [0.0 - 1.0]
    intensity = (r + g + b) / 3.0

    # 2. Saturation (S) [0.0 - 1.0]
    min_rgb = np.minimum(np.minimum(r, g), b)
    saturation = np.zeros_like(intensity)
    non_zero = intensity > 1e-6
    saturation[non_zero] = 1.0 - (min_rgb[non_zero] / intensity[non_zero])

    # 3. Hue (H) [0 - 360 derece]
    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g)**2 + (r - b) * (g - b)) + 1e-8
    theta = np.arccos(np.clip(num / den, -1.0, 1.0)) * (180.0 / np.pi)

    hue = theta.copy()
    hue[b > g] = 360.0 - theta[b > g]

    # 8-bit [0, 255] aralığına ölçekleme
    # Hue: [0, 360) -> [0, 255]
    h_8u = np.clip(np.round((hue / 360.0) * 255.0), 0, 255).astype(np.uint8)
    s_8u = np.clip(np.round(saturation * 255.0), 0, 255).astype(np.uint8)
    i_8u = np.clip(np.round(intensity * 255.0), 0, 255).astype(np.uint8)

    return np.dstack([h_8u, s_8u, i_8u])


def get_channel_stats(img_3c):
    """3 kanallı görüntünün her kanalı için min, max, ortalama ve standart sapmayı döner."""
    stats = []
    for c in range(3):
        ch = img_3c[:, :, c]
        stats.append({
            "min": int(np.min(ch)),
            "max": int(np.max(ch)),
            "mean": float(np.mean(ch)),
            "std": float(np.std(ch))
        })
    return stats


def main():
    parser = argparse.ArgumentParser(description="Renk Uzayı Dönüşümleri (HSV, HSI, YUV, CIE Lab) ve BMP Kaydetme")
    parser.add_argument("--input", default="../girdi/renkli_1000x1000.bmp", help="Girdi renkli BMP yolu")
    parser.add_argument("--outdir", default="cikti", help="Çıktı klasörü")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.normpath(os.path.join(script_dir, args.input))
    cikti_dir = os.path.normpath(os.path.join(script_dir, args.outdir))
    os.makedirs(cikti_dir, exist_ok=True)

    print("================================================================================")
    print("   ÖDEV 7.3: RENK UZAYLARI DÖNÜŞÜMÜ (HSV, HSI, YUV, CIE LAB) VE BMP KAYDETME    ")
    print("================================================================================")

    # 1. Girdi Görüntüsünü Aç
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {input_path}")

    resim_bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if resim_bgr is None:
        raise ValueError(f"OpenCV görüntüyü açamadı: {input_path}")

    h, w, c = resim_bgr.shape
    fsize_in = os.path.getsize(input_path)
    print(f"\n[1] Girdi Görüntüsü Yüklendi:")
    print(f"    - Dosya: {input_path}")
    print(f"    - Çözünürlük: {w} x {h} ({w*h:,} piksel)")
    print(f"    - Kanal Sayısı: {c} (BGR)")
    print(f"    - Dosya Boyutu: {fsize_in:,} bayt ({fsize_in / (1024*1024):.2f} MB)")

    # 2. Renk Uzayı Dönüşümleri
    print("\n[2] Renk Uzayı Dönüşümleri Hesaplanıyor...")

    # 2.1. HSV (Hue, Saturation, Value)
    print("    -> 1/4: HSV Dönüşümü (cv2.COLOR_BGR2HSV)...")
    resim_hsv = cv2.cvtColor(resim_bgr, cv2.COLOR_BGR2HSV)

    # 2.2. HSI (Hue, Saturation, Intensity) - Özel Fonksiyon
    print("    -> 2/4: HSI Dönüşümü (Gonzalez & Woods Kuramsal Formülü)...")
    resim_hsi = bgr_to_hsi(resim_bgr)

    # 2.3. YUV (Luma Y, U-Chroma, V-Chroma)
    print("    -> 3/4: YUV Dönüşümü (cv2.COLOR_BGR2YUV)...")
    resim_yuv = cv2.cvtColor(resim_bgr, cv2.COLOR_BGR2YUV)

    # 2.4. CIE L*a*b* (L*: Lightness, a*: Green-Red, b*: Blue-Yellow)
    print("    -> 4/4: CIE L*a*b* Dönüşümü (cv2.COLOR_BGR2LAB)...")
    resim_lab = cv2.cvtColor(resim_bgr, cv2.COLOR_BGR2LAB)

    donusumler = {
        "HSV": {
            "img": resim_hsv,
            "filename": "resim_hsv.bmp",
            "channels": ["Ton (Hue: 0-180)", "Doygunluk (Saturation: 0-255)", "Değer (Value: 0-255)"],
            "desc": "Silindirik Model: V = max(R,G,B). Işık şiddetinden bağımsız renk segmentasyonu."
        },
        "HSI": {
            "img": resim_hsi,
            "filename": "resim_hsi.bmp",
            "channels": ["Ton (Hue: 0-255)", "Doygunluk (Saturation: 0-255)", "Şiddet (Intensity: 0-255)"],
            "desc": "Çift Konik Model: I = (R+G+B)/3 ortalama luma enerjisi. Klasik literatür standardı."
        },
        "YUV": {
            "img": resim_yuv,
            "filename": "resim_yuv.bmp",
            "channels": ["Aydınlık (Luma Y: 0-255)", "Krominans U (Mavi Farkı)", "Krominans V (Kırmızı Farkı)"],
            "desc": "Yayın & Sıkıştırma: Luma renkten ayrık, video kodekleri (H.264/HEVC) için kroma alt örnekleme."
        },
        "CIE Lab": {
            "img": resim_lab,
            "filename": "resim_cielab.bmp",
            "channels": ["Algısal Parlaklık (L*: 0-255)", "Kromatik a* (Yeşil <-> Kırmızı)", "Kromatik b* (Mavi <-> Sarı)"],
            "desc": "Algısal Düzgün Uzay: Öklid mesafesi algılanan renk farkına (Delta E) tam orantılıdır."
        }
    }

    # 3. Her Birini BMP Formatında Kaydet
    print("\n[3] Dönüştürülen Görüntüler BMP Formatında Kaydediliyor...")
    saved_files = {}
    for name, info in donusumler.items():
        out_filepath = os.path.join(cikti_dir, info["filename"])
        # BMP olarak yaz (uint8 3 kanal)
        cv2.imwrite(out_filepath, info["img"])
        fsize = os.path.getsize(out_filepath)
        saved_files[name] = {
            "path": out_filepath,
            "size": fsize
        }
        print(f"    - {name:<10}: {out_filepath} ({fsize:,} bayt / {fsize/(1024*1024):.2f} MB)")

    # 4. Sayısal ve İstatistiksel Rapor
    print("\n[4] Kanal İstatistikleri ve Rapor Oluşturuluyor...")
    rapor_path = os.path.join(cikti_dir, "donusum_raporu.txt")
    with open(rapor_path, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("    ÖDEV 7.3: RENK UZAYI DÖNÜŞÜMLERİ (HSV, HSI, YUV, CIE LAB) RAPORU            \n")
        f.write("================================================================================\n\n")
        f.write(f"Tarih: 16 Kasım 2026\n")
        f.write(f"Girdi Dosyası: {input_path} ({w}x{h}, 3 Kanal BGR, {fsize_in:,} bayt)\n\n")
        
        f.write("1. ÜRETİLEN BMP DOSYALARI VE BOYUTLARI\n")
        f.write("   -----------------------------------------------------------------------------\n")
        f.write(f"   {'Renk Uzayı':<15} | {'Dosya Adı':<20} | {'Disk Boyutu':<18} | {'Durum':<10}\n")
        f.write("   -----------------------------------------------------------------------------\n")
        for name, sinfo in saved_files.items():
            f.write(f"   {name:<15} | {os.path.basename(sinfo['path']):<20} | {sinfo['size']:,} bayt ({sinfo['size']/(1024*1024):.2f} MB) | Başarılı\n")
        f.write("   -----------------------------------------------------------------------------\n\n")

        f.write("2. KANAL DÜZEYİNDE İSTATİSTİKSEL ANALİZ (Min, Max, Ortalama, Std. Sapma)\n")
        for name, info in donusumler.items():
            f.write(f"\n   [*] {name} Uzayı Kanalları:\n")
            stats = get_channel_stats(info["img"])
            for c_idx, ch_name in enumerate(info["channels"]):
                st = stats[c_idx]
                f.write(f"       - Kanal {c_idx} ({ch_name}):\n")
                f.write(f"         Min: {st['min']:>3} | Max: {st['max']:>3} | Ort: {st['mean']:>6.2f} | Std: {st['std']:>6.2f}\n")

        f.write("\n3. HSV İLE HSI ARASINDAKİ TEMEL FARKLAR\n")
        f.write("   - HSV'de Değer (Value): V = max(R, G, B) formülüyle hesaplanır. Üç renkten en yükseğini alır.\n")
        f.write("   - HSI'de Şiddet (Intensity): I = (R + G + B) / 3 formülüyle hesaplanır. Ortalama enerjidir.\n")
        f.write("   - Doygunluk Tanımları:\n")
        f.write("     * S_HSV = (V - min(R, G, B)) / V\n")
        f.write("     * S_HSI = 1 - (min(R, G, B) / I)\n")
        f.write("   - Bu farktan ötürü HSV ve HSI görsel olarak benzer görünse de piksel değerleri sayısal olarak\n")
        f.write("     farklıdır ve HSI insan algısındaki ışık enerjisini (luma) daha dengeli modeller.\n\n")

        f.write("4. KURAMSAL DÖNÜŞÜM FORMÜLLERİ\n")
        f.write("   - BGR -> YUV:\n")
        f.write("     Y =  0.299*R + 0.587*G + 0.114*B\n")
        f.write("     U = -0.147*R - 0.289*G + 0.436*B + 128 = 0.492*(B - Y) + 128\n")
        f.write("     V =  0.615*R - 0.515*G - 0.100*B + 128 = 0.877*(R - Y) + 128\n\n")
        f.write("   - BGR -> CIE L*a*b*:\n")
        f.write("     Önce BGR -> CIE XYZ standart beyaz nokta D65 referansıyla dönüştürülür;\n")
        f.write("     Ardından L* = 116 * f(Y/Yn) - 16, a* = 500 * [f(X/Xn) - f(Y/Yn)], b* = 200 * [f(Y/Yn) - f(Z/Zn)]\n")
        f.write("     bağıntılarıyla algısal düzgün küreye izdüşürülür.\n")

    print(f"    - Sayısal dönüşüm raporu kaydedildi: {rapor_path}")

    # 5. Kapsamlı Görselleştirme Paneli (5 Satır x 4 Sütun Grid)
    print("\n[5] Karşılaştırmalı Görsel Panel (5x4 Grid) Oluşturuluyor...")
    fig, axes = plt.subplots(5, 4, figsize=(18, 22))

    # Satır 0: BGR / RGB
    resim_rgb = cv2.cvtColor(resim_bgr, cv2.COLOR_BGR2RGB)
    axes[0, 0].imshow(resim_rgb)
    axes[0, 0].set_title("Orijinal Renkli (RGB Bileşimi)", fontweight="bold", fontsize=11)
    axes[0, 0].axis("off")
    axes[0, 1].imshow(resim_rgb[:, :, 0], cmap="Reds")
    axes[0, 1].set_title("RGB: Kırmızı (Red) Kanalı", fontweight="bold", fontsize=10)
    axes[0, 1].axis("off")
    axes[0, 2].imshow(resim_rgb[:, :, 1], cmap="Greens")
    axes[0, 2].set_title("RGB: Yeşil (Green) Kanalı", fontweight="bold", fontsize=10)
    axes[0, 2].axis("off")
    axes[0, 3].imshow(resim_rgb[:, :, 2], cmap="Blues")
    axes[0, 3].set_title("RGB: Mavi (Blue) Kanalı", fontweight="bold", fontsize=10)
    axes[0, 3].axis("off")

    # Satır 1: HSV
    # BMP olarak kaydedilen HSV 3-kanallı görseli direkt gösterim
    axes[1, 0].imshow(resim_hsv)
    axes[1, 0].set_title("1. HSV (Bileşik BMP Görseli)", fontweight="bold", fontsize=11)
    axes[1, 0].axis("off")
    axes[1, 1].imshow(resim_hsv[:, :, 0], cmap="hsv")
    axes[1, 1].set_title("HSV: Ton (Hue 0-180°)", fontweight="bold", fontsize=10)
    axes[1, 1].axis("off")
    axes[1, 2].imshow(resim_hsv[:, :, 1], cmap="gray")
    axes[1, 2].set_title("HSV: Doygunluk (Saturation 0-255)", fontweight="bold", fontsize=10)
    axes[1, 2].axis("off")
    axes[1, 3].imshow(resim_hsv[:, :, 2], cmap="gray")
    axes[1, 3].set_title("HSV: Parlaklık (Value: max(R,G,B))", fontweight="bold", fontsize=10)
    axes[1, 3].axis("off")

    # Satır 2: HSI
    axes[2, 0].imshow(resim_hsi)
    axes[2, 0].set_title("2. HSI (Bileşik BMP Görseli)", fontweight="bold", fontsize=11)
    axes[2, 0].axis("off")
    axes[2, 1].imshow(resim_hsi[:, :, 0], cmap="hsv")
    axes[2, 1].set_title("HSI: Ton (Hue 0-255)", fontweight="bold", fontsize=10)
    axes[2, 1].axis("off")
    axes[2, 2].imshow(resim_hsi[:, :, 1], cmap="gray")
    axes[2, 2].set_title("HSI: Doygunluk (Saturation 0-255)", fontweight="bold", fontsize=10)
    axes[2, 2].axis("off")
    axes[2, 3].imshow(resim_hsi[:, :, 2], cmap="gray")
    axes[2, 3].set_title("HSI: Şiddet (Intensity: (R+G+B)/3)", fontweight="bold", fontsize=10)
    axes[2, 3].axis("off")

    # Satır 3: YUV
    axes[3, 0].imshow(resim_yuv)
    axes[3, 0].set_title("3. YUV (Bileşik BMP Görseli)", fontweight="bold", fontsize=11)
    axes[3, 0].axis("off")
    axes[3, 1].imshow(resim_yuv[:, :, 0], cmap="gray")
    axes[3, 1].set_title("YUV: Aydınlık (Luma Y)", fontweight="bold", fontsize=10)
    axes[3, 1].axis("off")
    axes[3, 2].imshow(resim_yuv[:, :, 1], cmap="coolwarm")
    axes[3, 2].set_title("YUV: Krominans U (Mavi Farkı)", fontweight="bold", fontsize=10)
    axes[3, 2].axis("off")
    axes[3, 3].imshow(resim_yuv[:, :, 2], cmap="coolwarm")
    axes[3, 3].set_title("YUV: Krominans V (Kırmızı Farkı)", fontweight="bold", fontsize=10)
    axes[3, 3].axis("off")

    # Satır 4: CIE Lab
    axes[4, 0].imshow(resim_lab)
    axes[4, 0].set_title("4. CIE L*a*b* (Bileşik BMP Görseli)", fontweight="bold", fontsize=11)
    axes[4, 0].axis("off")
    axes[4, 1].imshow(resim_lab[:, :, 0], cmap="gray")
    axes[4, 1].set_title("CIE Lab: Algısal Aydınlık (L*)", fontweight="bold", fontsize=10)
    axes[4, 1].axis("off")
    axes[4, 2].imshow(resim_lab[:, :, 1], cmap="RdYlGn_r")
    axes[4, 2].set_title("CIE Lab: a* Kanalı (Yeşil <-> Kırmızı)", fontweight="bold", fontsize=10)
    axes[4, 2].axis("off")
    axes[4, 3].imshow(resim_lab[:, :, 2], cmap="YlGnBu_r")
    axes[4, 3].set_title("CIE Lab: b* Kanalı (Mavi <-> Sarı)", fontweight="bold", fontsize=10)
    axes[4, 3].axis("off")

    plt.suptitle("Ödev 7.3: Renkli BMP Görüntüsünün Renk Uzaylarına Dönüştürülmesi (HSV, HSI, YUV, CIE Lab)\n"
                 "[Her Bir Renk Uzayı 3-Kanallı 24-bit BMP Olarak Kaydedilmiştir]",
                 fontsize=15, fontweight="bold")
    plt.tight_layout()
    panel_path = os.path.join(cikti_dir, "renk_uzaylari_paneli.png")
    plt.savefig(panel_path, dpi=200)
    plt.close()
    print(f"    - Renk uzayları paneli kaydedildi: {panel_path}")

    print("\n================================================================================")
    print("   ÖDEV 7.3 BAŞARIYLA TAMAMLANDI!")
    print("================================================================================")


if __name__ == "__main__":
    main()
