#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ödev 7.1: Renk Uzayları Araştırması ve 1000x1000 BMP Dosya Boyutu / Kanal Analizi
Ders: Görüntü İşleme
Tarih: 16 Kasım 2026

Bu betik:
1. 1000x1000 boyutundaki 24-bit renkli BMP görüntüsünü açar ve inceler.
2. OpenCV cv2.imshow ile ekranda gösterim desteği sunar (ekran yoksa güvenle atlar).
3. Görüntüyü ITU-R BT.601 standart formülü (Y = 0.299R + 0.587G + 0.114B) ve cv2.cvtColor ile gri tonlamaya çevirir.
4. Gri seviye görüntüyü 8-bit BMP formatında kaydeder.
5. Disk boyutu, çözünürlük, kanal sayısı, BMP başlıkları (Header, DIB, Palet) ve piksel dizisi boyutlarını ayrıntılı analiz eder.
6. Renk uzaylarını (RGB, HSV, YUV, CIE Lab) görselleştirir ve analiz raporu üretir.
"""

import os
import sys
import struct
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt


def parse_bmp_header(file_path):
    """
    BMP dosyasının ikili (binary) başlık yapısını çözümler.
    - BITMAPFILEHEADER (14 bayt)
    - BITMAPINFOHEADER (40 bayt)
    - Renk Paleti (Varsa 256 x 4 = 1024 bayt)
    """
    with open(file_path, "rb") as f:
        header_bytes = f.read(54)
    
    if len(header_bytes) < 54:
        raise ValueError(f"Geçersiz BMP dosyası: {file_path}")
    
    # BITMAPFILEHEADER (14 bayt): bfType(2s), bfSize(I), bfReserved1(H), bfReserved2(H), bfOffBits(I)
    bfType, bfSize, bfRes1, bfRes2, bfOffBits = struct.unpack("<2sIHHI", header_bytes[:14])
    
    # BITMAPINFOHEADER (40 bayt): biSize(I), biWidth(i), biHeight(i), biPlanes(H), biBitCount(H), biCompression(I), biSizeImage(I), biXPels(i), biYPels(i), biClrUsed(I), biClrImportant(I)
    (biSize, biWidth, biHeight, biPlanes, biBitCount,
     biCompression, biSizeImage, biXPels, biYPels,
     biClrUsed, biClrImportant) = struct.unpack("<IiiHHIIiiII", header_bytes[14:54])
    
    actual_file_size = os.path.getsize(file_path)
    palette_size = bfOffBits - 54 if bfOffBits > 54 else 0
    num_palette_entries = palette_size // 4
    
    # Satır hizalaması (4 bayt sınırına yuvarlama - padding hesabı)
    row_data_bytes = (biWidth * biBitCount) // 8
    row_stride = ((biWidth * biBitCount + 31) // 32) * 4
    padding_per_row = row_stride - row_data_bytes
    total_pixel_data_size = row_stride * abs(biHeight)
    
    return {
        "signature": bfType.decode("latin1", errors="ignore"),
        "header_file_size": bfSize,
        "actual_disk_size": actual_file_size,
        "data_offset": bfOffBits,
        "dib_header_size": biSize,
        "width": biWidth,
        "height": abs(biHeight),
        "planes": biPlanes,
        "bit_count": biBitCount,
        "channels": biBitCount // 8,
        "compression": biCompression,
        "image_data_size": biSizeImage,
        "palette_size": palette_size,
        "num_palette_entries": num_palette_entries,
        "row_data_bytes": row_data_bytes,
        "row_stride": row_stride,
        "padding_per_row": padding_per_row,
        "total_pixel_data_size": total_pixel_data_size
    }


def custom_bgr_to_gray(bgr_img):
    """
    ITU-R BT.601 standart luma ağırlıkları ile sıfırdan Gri Seviye dönüşümü:
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    """
    b = bgr_img[:, :, 0].astype(np.float32)
    g = bgr_img[:, :, 1].astype(np.float32)
    r = bgr_img[:, :, 2].astype(np.float32)
    gray = 0.114 * b + 0.587 * g + 0.299 * r
    return np.clip(np.round(gray), 0, 255).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(description="1000x1000 Renkli BMP -> Gri Tonlama ve Boyut Analizi")
    parser.add_argument("--input", default="../girdi/renkli_1000x1000.bmp", help="Girdi renkli BMP yolu")
    parser.add_argument("--output-gray", default="cikti/gri_1000x1000.bmp", help="Cikti gri BMP yolu")
    parser.add_argument("--show", action="store_true", help="cv2.imshow ile ekranda pencereli goster")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.normpath(os.path.join(script_dir, args.input))
    output_gray_path = os.path.normpath(os.path.join(script_dir, args.output_gray))
    cikti_dir = os.path.dirname(output_gray_path)
    os.makedirs(cikti_dir, exist_ok=True)

    print("================================================================================")
    print("   ÖDEV 7.1: RENK UZAYLARI VE 1000x1000 BMP DOSYA BOYUTU / KANAL ANALİZİ        ")
    print("================================================================================")

    # 1. Görüntüyü Oku
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {input_path}")

    resim_renkli = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if resim_renkli is None:
        raise ValueError(f"OpenCV görüntüyü yükleyemedi: {input_path}")

    h, w, c = resim_renkli.shape
    print(f"\n[1] Girdi Görüntüsü Yüklendi:")
    print(f"    - Dosya: {input_path}")
    print(f"    - Çözünürlük: {w} x {h}")
    print(f"    - Toplam Piksel: {w * h:,} piksel")
    print(f"    - Kanal Sayısı: {c} (BGR - Mavi, Yeşil, Kırmızı)")
    print(f"    - Veri Tipi: {resim_renkli.dtype} (Piksel başına 8-bit unsigned)")

    # 2. Ekranda Gösterim (GUI)
    if args.show:
        try:
            print("\n[2] Ekranda Gösteriliyor (Pencereyi kapatmak için herhangi bir tuşa basınız)...")
            cv2.namedWindow("1000x1000 Renkli BMP Goruntu", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("1000x1000 Renkli BMP Goruntu", 800, 800)
            cv2.imshow("1000x1000 Renkli BMP Goruntu", resim_renkli)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except cv2.error as e:
            print(f"    [UYARI] GUI desteği bulunamadı veya headless ortam: {e}")
    else:
        print("\n[2] Ekranda Gösterim: '--show' argümanı verilmedi; görsel matplotlib ile PNG olarak kaydedilecek.")

    # 3. Gri Tonlamaya Dönüştürme
    print("\n[3] Gri Tonlamaya Dönüştürme:")
    resim_gri_cv = cv2.cvtColor(resim_renkli, cv2.COLOR_BGR2GRAY)
    resim_gri_custom = custom_bgr_to_gray(resim_renkli)

    # Doğrulama: OpenCV ile özel dönüşüm arasındaki mutlak fark
    fark = np.abs(resim_gri_cv.astype(np.int32) - resim_gri_custom.astype(np.int32))
    mae = np.mean(fark)
    max_fark = np.max(fark)
    print(f"    - OpenCV cv2.cvtColor(..., cv2.COLOR_BGR2GRAY) uygulandı.")
    print(f"    - Özel Formül (Y = 0.299R + 0.587G + 0.114B) uygulandı.")
    print(f"    - İki yöntem arası Ortalama Mutlak Hata (MAE): {mae:.4f}")
    print(f"    - Maksimum Piksel Farkı: {max_fark} (yuvarlama hassasiyet sınırında)")

    # 4. Gri Görüntüyü BMP Olarak Kaydet
    cv2.imwrite(output_gray_path, resim_gri_cv)
    print(f"\n[4] Gri Görüntü Kaydedildi:")
    print(f"    - Çıktı Dosyası: {output_gray_path}")

    # 5. İkili (Binary) Başlık ve Disk Boyut Analizi
    renkli_meta = parse_bmp_header(input_path)
    gri_meta = parse_bmp_header(output_gray_path)

    oran = renkli_meta["actual_disk_size"] / gri_meta["actual_disk_size"]
    piksel_oran = renkli_meta["total_pixel_data_size"] / gri_meta["total_pixel_data_size"]

    print("\n[5] Karşılaştırmalı BMP Boyut Analizi:")
    print("--------------------------------------------------------------------------------")
    print(f"{'Özellik / Metrik':<32} | {'Renkli BMP (24-bit)':<20} | {'Gri Tonlu BMP (8-bit)':<20}")
    print("--------------------------------------------------------------------------------")
    print(f"{'Çözünürlük (Genişlik x Yükseklik)':<32} | {renkli_meta['width']} x {renkli_meta['height']:<13} | {gri_meta['width']} x {gri_meta['height']:<13}")
    print(f"{'Kanal Sayısı':<32} | {renkli_meta['channels']} kanal (BGR)         | {gri_meta['channels']} kanal (Luma)        ")
    print(f"{'Piksel Başına Bit (bpp)':<32} | {renkli_meta['bit_count']} bit (3 bayt)        | {gri_meta['bit_count']} bit (1 bayt)        ")
    print(f"{'BMP Başlık Boyutu (File+DIB)':<32} | 54 bayt              | 54 bayt              ")
    print(f"{'Renk Paleti Tablosu':<32} | {renkli_meta['palette_size']} bayt (Yok)          | {gri_meta['palette_size']} bayt (256x4 bayt)  ")
    print(f"{'Piksel Veri Başlangıç Ofseti':<32} | {renkli_meta['data_offset']} bayt              | {gri_meta['data_offset']} bayt            ")
    print(f"{'Satır Başına Bayt':<32} | {renkli_meta['row_data_bytes']} bayt            | {gri_meta['row_data_bytes']} bayt            ")
    print(f"{'Satır Dolgusu (4-bayt Padding)':<32} | {renkli_meta['padding_per_row']} bayt               | {gri_meta['padding_per_row']} bayt               ")
    print(f"{'Saf Piksel Verisi Boyutu':<32} | {renkli_meta['total_pixel_data_size']:,} bayt       | {gri_meta['total_pixel_data_size']:,} bayt       ")
    print(f"{'Toplam Disk Boyutu':<32} | {renkli_meta['actual_disk_size']:,} bayt       | {gri_meta['actual_disk_size']:,} bayt       ")
    print(f"{'Toplam Disk Boyutu (KB / MB)':<32} | {renkli_meta['actual_disk_size']/1024:.2f} KB ({renkli_meta['actual_disk_size']/(1024*1024):.2f} MB) | {gri_meta['actual_disk_size']/1024:.2f} KB ({gri_meta['actual_disk_size']/(1024*1024):.2f} MB)")
    print("--------------------------------------------------------------------------------")
    print(f"    * Saf Piksel Verisi Oranı (Renkli / Gri): {piksel_oran:.4f}x (Tam olarak 3.0 kat)")
    print(f"    * Toplam Disk Dosya Boyutu Oranı:         {oran:.4f}x (Yaklaşık 3.0 kat)")
    print(f"    * Disk Boyutu Farkı Nedeni: 24-bit'te her piksel 3 bayt (B, G, R) tutarken,")
    print(f"      8-bit'te tek bayttır. Gri BMP'deki 1024 baytlık fazlalık 256 renk paletidir.")

    # 6. Rapor Dosyasına Yazma
    rapor_path = os.path.join(cikti_dir, "boyut_analizi_raporu.txt")
    with open(rapor_path, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("       ÖDEV 7.1: 1000x1000 BMP RENKLİ VE GRİ SEVİYE BOYUT ANALİZ RAPORU         \n")
        f.write("================================================================================\n\n")
        f.write(f"Tarih: 16 Kasım 2026\n\n")
        f.write("1. GÖRÜNTÜ VE ÇÖZÜNÜRLÜK BİLGİLERİ\n")
        f.write(f"   - Görüntü Boyutları: {w} x {h}\n")
        f.write(f"   - Toplam Piksel Sayısı: {w * h:,} piksel\n\n")
        f.write("2. DOSYA VE BAŞLIK YAPISI KARŞILAŞTIRMASI\n")
        f.write("   -----------------------------------------------------------------------------\n")
        f.write(f"   {'Parametre':<30} | {'Renkli BMP (24-bit)':<20} | {'Gri BMP (8-bit)':<20}\n")
        f.write("   -----------------------------------------------------------------------------\n")
        f.write(f"   {'Kanal Sayısı':<30} | {renkli_meta['channels']} (BGR)                | {gri_meta['channels']} (Gri)\n")
        f.write(f"   {'Bit Derinliği':<30} | {renkli_meta['bit_count']} bit/piksel          | {gri_meta['bit_count']} bit/piksel\n")
        f.write(f"   {'BITMAPFILEHEADER':<30} | 14 bayt              | 14 bayt\n")
        f.write(f"   {'BITMAPINFOHEADER':<30} | 40 bayt              | 40 bayt\n")
        f.write(f"   {'Renk Paleti Tablosu':<30} | 0 bayt (Yok)         | 1024 bayt (256 x 4 bayt)\n")
        f.write(f"   {'Veri Başlangıç Ofseti':<30} | {renkli_meta['data_offset']} bayt              | {gri_meta['data_offset']} bayt\n")
        f.write(f"   {'Satır Hizalama (Padding)':<30} | {renkli_meta['padding_per_row']} bayt               | {gri_meta['padding_per_row']} bayt\n")
        f.write(f"   {'Piksel Matrisi Boyutu':<30} | {renkli_meta['total_pixel_data_size']:,} bayt       | {gri_meta['total_pixel_data_size']:,} bayt\n")
        f.write(f"   {'Toplam Disk Dosya Boyutu':<30} | {renkli_meta['actual_disk_size']:,} bayt       | {gri_meta['actual_disk_size']:,} bayt\n")
        f.write(f"   {'Disk Boyutu (KB)':<30} | {renkli_meta['actual_disk_size']/1024:.2f} KB            | {gri_meta['actual_disk_size']/1024:.2f} KB\n")
        f.write(f"   {'Disk Boyutu (MB)':<30} | {renkli_meta['actual_disk_size']/(1024*1024):.4f} MB          | {gri_meta['actual_disk_size']/(1024*1024):.4f} MB\n")
        f.write("   -----------------------------------------------------------------------------\n\n")
        f.write("3. MATEMATİKSEL İSPAT VE SONUÇ DEĞERLENDİRMESİ\n")
        f.write(f"   - Renkli BMP Dosya Boyutu Formülü:\n")
        f.write(f"     Boyut = 54 (Başlık) + (1000 x 1000 x 3 bayt piksel) = 3,000,054 bayt (~2.86 MB)\n")
        f.write(f"   - Gri BMP Dosya Boyutu Formülü:\n")
        f.write(f"     Boyut = 54 (Başlık) + 1024 (Palet) + (1000 x 1000 x 1 bayt piksel) = 1,001,078 bayt (~0.95 MB)\n")
        f.write(f"   - Boyut Oranı:\n")
        f.write(f"     3,000,054 / 1,001,078 = {oran:.4f} (Kanal sayısı 3'ten 1'e düştüğü için yaklaşık 3 kat azalma)\n")
        f.write(f"   - 3.0'dan küçük sapmanın nedeni: 8-bit formatında piksel indekslerini renk karşılıklarına\n")
        f.write(f"     bağlayan 1024 baytlık renk paleti (Color Palette / RGBQUAD[256]) tablosunun bulunmasıdır.\n")

    print(f"    - Sayısal analiz raporu kaydedildi: {rapor_path}")

    # 7. Renk Uzaylarına Dönüştürme ve Görselleştirme Paneli
    print("\n[6] Görselleştirme Panelleri Oluşturuluyor...")
    
    # 7.1. BMP Boyut ve Gri Dönüşüm Karşılaştırma Paneli
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Orijinal Renkli
    axes[0, 0].imshow(cv2.cvtColor(resim_renkli, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title(f"1. Orijinal 24-bit Renkli BMP\n(1000x1000, 3 Kanal, {renkli_meta['actual_disk_size']:,} bayt)", fontsize=11, fontweight="bold")
    axes[0, 0].axis("off")

    # Gri Seviye
    axes[0, 1].imshow(resim_gri_cv, cmap="gray")
    axes[0, 1].set_title(f"2. Gri Tonlamalı 8-bit BMP\n(1000x1000, 1 Kanal, {gri_meta['actual_disk_size']:,} bayt)", fontsize=11, fontweight="bold")
    axes[0, 1].axis("off")

    # Histogram Karşılaştırması
    hist_r = cv2.calcHist([resim_renkli], [2], None, [256], [0, 256])
    hist_g = cv2.calcHist([resim_renkli], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([resim_renkli], [0], None, [256], [0, 256])
    hist_gray = cv2.calcHist([resim_gri_cv], [0], None, [256], [0, 256])

    axes[1, 0].plot(hist_r, color="red", alpha=0.7, label="Kırmızı Kanal (R)")
    axes[1, 0].plot(hist_g, color="green", alpha=0.7, label="Yeşil Kanal (G)")
    axes[1, 0].plot(hist_b, color="blue", alpha=0.7, label="Mavi Kanal (B)")
    axes[1, 0].plot(hist_gray, color="black", linestyle="--", linewidth=1.5, label="Gri Seviye (Luma Y)")
    axes[1, 0].set_title("3. Renk Kanalları ve Gri Histogram Dağılımı", fontsize=11, fontweight="bold")
    axes[1, 0].set_xlabel("Piksel Yoğunluğu (0 - 255)")
    axes[1, 0].set_ylabel("Piksel Sayısı")
    axes[1, 0].set_xlim([0, 255])
    axes[1, 0].grid(True, linestyle=":", alpha=0.6)
    axes[1, 0].legend()

    # Boyut Karşılaştırma Grafiği (Bar Chart)
    categories = ["Piksel Verisi", "Toplam Dosya"]
    color_bytes = [renkli_meta["total_pixel_data_size"] / (1024*1024), renkli_meta["actual_disk_size"] / (1024*1024)]
    gray_bytes = [gri_meta["total_pixel_data_size"] / (1024*1024), gri_meta["actual_disk_size"] / (1024*1024)]

    x = np.arange(len(categories))
    width = 0.35
    rects1 = axes[1, 1].bar(x - width/2, color_bytes, width, label="Renkli BMP (24-bit / 3 Kanal)", color="#e74c3c")
    rects2 = axes[1, 1].bar(x + width/2, gray_bytes, width, label="Gri BMP (8-bit / 1 Kanal)", color="#7f8c8d")

    axes[1, 1].set_title("4. Disk Boyutu Kıyaslaması (Megabayt)", fontsize=11, fontweight="bold")
    axes[1, 1].set_ylabel("Boyut (MB)")
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(categories, fontweight="bold")
    axes[1, 1].legend()
    axes[1, 1].grid(True, axis="y", linestyle=":", alpha=0.6)

    for rect in rects1:
        h_val = rect.get_height()
        axes[1, 1].annotate(f"{h_val:.2f} MB", xy=(rect.get_x() + rect.get_width()/2, h_val),
                            xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")
    for rect in rects2:
        h_val = rect.get_height()
        axes[1, 1].annotate(f"{h_val:.2f} MB", xy=(rect.get_x() + rect.get_width()/2, h_val),
                            xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

    plt.suptitle("Ödev 7.1: 1000x1000 BMP Renkli ve Gri Seviye Boyut / Kanal Analizi", fontsize=14, fontweight="bold")
    plt.tight_layout()
    gorsel_path = os.path.join(cikti_dir, "karsilastirma_gorsel.png")
    plt.savefig(gorsel_path, dpi=200)
    plt.close()
    print(f"    - BMP karşılaştırma görseli kaydedildi: {gorsel_path}")

    # 7.2. Renk Uzayları Ayrıştırma Paneli (RGB, HSV, YUV, CIE Lab)
    print("    - Renk Uzayları ayrıştırma paneli hazırlanıyor (RGB, HSV, YUV, CIE Lab)...")
    hsv_img = cv2.cvtColor(resim_renkli, cv2.COLOR_BGR2HSV)
    yuv_img = cv2.cvtColor(resim_renkli, cv2.COLOR_BGR2YUV)
    lab_img = cv2.cvtColor(resim_renkli, cv2.COLOR_BGR2LAB)

    fig_spaces, axes_spaces = plt.subplots(4, 3, figsize=(14, 16))
    
    # 1. Satır: RGB
    axes_spaces[0, 0].imshow(resim_renkli[:, :, 2], cmap="Reds")
    axes_spaces[0, 0].set_title("RGB: Kırmızı (Red) Kanalı", fontweight="bold")
    axes_spaces[0, 0].axis("off")
    axes_spaces[0, 1].imshow(resim_renkli[:, :, 1], cmap="Greens")
    axes_spaces[0, 1].set_title("RGB: Yeşil (Green) Kanalı", fontweight="bold")
    axes_spaces[0, 1].axis("off")
    axes_spaces[0, 2].imshow(resim_renkli[:, :, 0], cmap="Blues")
    axes_spaces[0, 2].set_title("RGB: Mavi (Blue) Kanalı", fontweight="bold")
    axes_spaces[0, 2].axis("off")

    # 2. Satır: HSV
    axes_spaces[1, 0].imshow(hsv_img[:, :, 0], cmap="hsv")
    axes_spaces[1, 0].set_title("HSV: Ton (Hue - 0-180°)", fontweight="bold")
    axes_spaces[1, 0].axis("off")
    axes_spaces[1, 1].imshow(hsv_img[:, :, 1], cmap="gray")
    axes_spaces[1, 1].set_title("HSV: Doygunluk (Saturation - 0-255)", fontweight="bold")
    axes_spaces[1, 1].axis("off")
    axes_spaces[1, 2].imshow(hsv_img[:, :, 2], cmap="gray")
    axes_spaces[1, 2].set_title("HSV: Parlaklık (Value - 0-255)", fontweight="bold")
    axes_spaces[1, 2].axis("off")

    # 3. Satır: YUV
    axes_spaces[2, 0].imshow(yuv_img[:, :, 0], cmap="gray")
    axes_spaces[2, 0].set_title("YUV: Aydınlık (Luma Y)", fontweight="bold")
    axes_spaces[2, 0].axis("off")
    axes_spaces[2, 1].imshow(yuv_img[:, :, 1], cmap="coolwarm")
    axes_spaces[2, 1].set_title("YUV: Krominans U (Mavi Farkı)", fontweight="bold")
    axes_spaces[2, 1].axis("off")
    axes_spaces[2, 2].imshow(yuv_img[:, :, 2], cmap="coolwarm")
    axes_spaces[2, 2].set_title("YUV: Krominans V (Kırmızı Farkı)", fontweight="bold")
    axes_spaces[2, 2].axis("off")

    # 4. Satır: CIE Lab
    axes_spaces[3, 0].imshow(lab_img[:, :, 0], cmap="gray")
    axes_spaces[3, 0].set_title("CIE Lab: Algısal Aydınlık (L*)", fontweight="bold")
    axes_spaces[3, 0].axis("off")
    axes_spaces[3, 1].imshow(lab_img[:, :, 1], cmap="RdYlGn_r")
    axes_spaces[3, 1].set_title("CIE Lab: a* Kanalı (Yeşil <-> Kırmızı)", fontweight="bold")
    axes_spaces[3, 1].axis("off")
    axes_spaces[3, 2].imshow(lab_img[:, :, 2], cmap="YlGnBu_r")
    axes_spaces[3, 2].set_title("CIE Lab: b* Kanalı (Mavi <-> Sarı)", fontweight="bold")
    axes_spaces[3, 2].axis("off")

    plt.suptitle("Görüntü İşlemede Renk Uzaylarının Kanallarına Ayrıştırılması", fontsize=15, fontweight="bold")
    plt.tight_layout()
    uzaylar_gorsel_path = os.path.join(cikti_dir, "renk_uzaylari_karsilastirma.png")
    plt.savefig(uzaylar_gorsel_path, dpi=200)
    plt.close()
    print(f"    - Renk uzayları görsel paneli kaydedildi: {uzaylar_gorsel_path}")

    print("\n================================================================================")
    print("   ÖDEV 7.1 BAŞARIYLA TAMAMLANDI!")
    print("================================================================================")


if __name__ == "__main__":
    main()
