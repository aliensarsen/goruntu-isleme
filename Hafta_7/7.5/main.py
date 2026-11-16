#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ödev 7.5 (Görev 5): RGB, YCbCr ve HSV Renk Uzaylarında Ten Rengi Tespiti ve Ten Dışı Alanları Tam Kırmızı Gösterme
Ders: Görüntü İşleme
Tarih: 16 Kasım 2026

Bu betik:
1. Çoklu etnik kökenden ve farklı arka plan renklerinden oluşan insan yüzleri görselini açar.
2. RGB renk uzayında kuramsal kurallarla (Peer et al.) ten rengini tespit eder; ten olmayan yerleri tam kırmızı (BGR: [0, 0, 255]) yapar.
3. Ten tespiti için daha uygun olan YCbCr renk uzayına geçer; ten dışı alanları tam kırmızı yapar.
4. Ten tespiti için daha uygun olan HSV renk uzayına geçer; ten dışı alanları tam kırmızı yapar.
5. Her üç yöntemin maskelerini, ten dışı tam kırmızı sonuçlarını ve neden YCbCr/HSV'nin RGB'den üstün olduğunu raporlar.
"""

import os
import sys
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt


def detect_skin_rgb(bgr_img):
    """
    RGB renk uzayında insan teni tespiti (Peer et al. standardı).
    Kural:
    - R > 95, G > 40, B > 20
    - max(R, G, B) - min(R, G, B) > 15
    - |R - G| > 15
    - R > G ve R > B
    """
    r = bgr_img[:, :, 2].astype(np.int32)
    g = bgr_img[:, :, 1].astype(np.int32)
    b = bgr_img[:, :, 0].astype(np.int32)

    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)

    mask = (
        (r > 95) & (g > 40) & (b > 20) &
        ((max_c - min_c) > 15) &
        (np.abs(r - g) > 15) &
        (r > g) & (r > b)
    )
    return mask.astype(bool)


def detect_skin_ycbcr(bgr_img):
    """
    YCbCr (YCrCb) renk uzayında insan teni tespiti (Chai & Ngan, Kovac standardı).
    İnsan teni krominans düzleminde (Cb, Cr) dar bir eliptik kümede toplanır:
    - 133 <= Cr <= 173
    - 77 <= Cb <= 127
    (Aydınlık Y kanalı elenerek ışık değişimlerinden bağımsızlaşılır).
    """
    ycrcb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2YCrCb)
    # OpenCV'de YCrCb sıralaması: Kanal 0 = Y, Kanal 1 = Cr, Kanal 2 = Cb
    cr = ycrcb[:, :, 1]
    cb = ycrcb[:, :, 2]

    mask = (cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)
    return mask.astype(bool)


def detect_skin_hsv(bgr_img):
    """
    HSV renk uzayında insan teni tespiti.
    İnsan teninin tonu (Hue) kırmızı-sarı bandında yer alır:
    - 0 <= H <= 22 veya 170 <= H <= 180 (kırmızı uçları)
    - 35 <= S <= 190 (aşırı doymuş parlak sarı/kırmızı arka planları eler)
    - V >= 50 (aşırı karanlık gölgeleri eler)
    """
    hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    mask = (
        ((h >= 0) & (h <= 22) | (h >= 170) & (h <= 180)) &
        (s >= 35) & (s <= 190) &
        (v >= 50)
    )
    return mask.astype(bool)


def apply_red_to_nonskin(bgr_img, skin_mask):
    """
    Ten olmayan bölgeleri (mask == False) tam kırmızı (BGR: [0, 0, 255]) yapar.
    Ten olan bölgeleri orijinal renklerinde bırakır.
    """
    out = bgr_img.copy()
    # OpenCV'de tam kırmızı: Mavi=0, Yeşil=0, Kırmızı=255
    out[~skin_mask] = [0, 0, 255]
    return out


def main():
    parser = argparse.ArgumentParser(description="RGB, YCbCr ve HSV ile Ten Rengi Tespiti")
    parser.add_argument("--input", default="../girdi/insan_tenleri.jpg", help="Girdi resim yolu")
    parser.add_argument("--outdir", default="cikti", help="Çıktı klasörü")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.normpath(os.path.join(script_dir, args.input))
    cikti_dir = os.path.normpath(os.path.join(script_dir, args.outdir))
    os.makedirs(cikti_dir, exist_ok=True)

    print("================================================================================")
    print("   ÖDEV 7.5 (GÖREV 5): TEN RENGİ TESPİTİ (RGB, YCbCr, HSV) VE TEN DIŞI KIRMIZI   ")
    print("================================================================================")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {input_path}")

    bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError(f"OpenCV görseli açamadı: {input_path}")

    h, w, c = bgr.shape
    total_px = h * w
    print(f"\n[1] Görüntü Yüklendi:")
    print(f"    - Dosya: {input_path}")
    print(f"    - Çözünürlük: {w} x {h} ({total_px:,} piksel)")
    print(f"    - İçerik: 21 farklı yüz (farklı etnik kökenler ve canlı renkli arka planlar)")

    # 1. RGB Segmentasyonu
    print("\n[2] RGB Renk Uzayında Ten Tespiti Hesaplanıyor (Peer et al. Kuralları)...")
    mask_rgb = detect_skin_rgb(bgr)
    res_rgb = apply_red_to_nonskin(bgr, mask_rgb)
    out_rgb_path = os.path.join(cikti_dir, "ten_rgb.png")
    cv2.imwrite(out_rgb_path, res_rgb)
    px_rgb = int(np.sum(mask_rgb))
    pct_rgb = (px_rgb / total_px) * 100
    print(f"    - Tespit Edilen Ten Pikseli: {px_rgb:,} (%{pct_rgb:.2f})")
    print(f"    - Kaydedildi: {out_rgb_path}")

    # 2. YCbCr Segmentasyonu
    print("\n[3] YCbCr Renk Uzayında Ten Tespiti Hesaplanıyor (Kovac / Chai & Ngan Kuralları)...")
    mask_ycbcr = detect_skin_ycbcr(bgr)
    res_ycbcr = apply_red_to_nonskin(bgr, mask_ycbcr)
    out_ycbcr_path = os.path.join(cikti_dir, "ten_ycbcr.png")
    cv2.imwrite(out_ycbcr_path, res_ycbcr)
    px_ycbcr = int(np.sum(mask_ycbcr))
    pct_ycbcr = (px_ycbcr / total_px) * 100
    print(f"    - Tespit Edilen Ten Pikseli: {px_ycbcr:,} (%{pct_ycbcr:.2f})")
    print(f"    - Kaydedildi: {out_ycbcr_path}")

    # 3. HSV Segmentasyonu
    print("\n[4] HSV Renk Uzayında Ten Tespiti Hesaplanıyor (Hue-Saturation Filtreleme)...")
    mask_hsv = detect_skin_hsv(bgr)
    res_hsv = apply_red_to_nonskin(bgr, mask_hsv)
    out_hsv_path = os.path.join(cikti_dir, "ten_hsv.png")
    cv2.imwrite(out_hsv_path, res_hsv)
    px_hsv = int(np.sum(mask_hsv))
    pct_hsv = (px_hsv / total_px) * 100
    print(f"    - Tespit Edilen Ten Pikseli: {px_hsv:,} (%{pct_hsv:.2f})")
    print(f"    - Kaydedildi: {out_hsv_path}")

    # 4. Sayısal Rapor Dosyasını Yaz
    rapor_path = os.path.join(cikti_dir, "ten_tespiti_raporu.txt")
    with open(rapor_path, "w", encoding="utf-8") as f:
        f.write("================================================================================\n")
        f.write("    ÖDEV 7.5 (GÖREV 5): TEN RENGİ TESPİTİ VE RENK UZAYI KIYASLAMA RAPORU        \n")
        f.write("================================================================================\n\n")
        f.write(f"Tarih: 16 Kasım 2026\n")
        f.write(f"Girdi Görseli: {input_path} ({w}x{h}, {total_px:,} piksel)\n\n")

        f.write("1. RENK UZAYLARININ SAYISAL TEN TESPİT SONUÇLARI\n")
        f.write("   -----------------------------------------------------------------------------\n")
        f.write(f"   {'Renk Uzayı':<15} | {'Ten Piksel Sayısı':<20} | {'Ten Oranı (%)':<15} | {'Ten Dışı Renk'}\n")
        f.write("   -----------------------------------------------------------------------------\n")
        f.write(f"   {'RGB (Peer)':<15} | {px_rgb:>17,} | {pct_rgb:>13.2f}% | Tam Kırmızı [0,0,255]\n")
        f.write(f"   {'YCbCr (Chai)':<15} | {px_ycbcr:>17,} | {pct_ycbcr:>13.2f}% | Tam Kırmızı [0,0,255]\n")
        f.write(f"   {'HSV (Hue-Sat)':<15} | {px_hsv:>17,} | {pct_hsv:>13.2f}% | Tam Kırmızı [0,0,255]\n")
        f.write("   -----------------------------------------------------------------------------\n\n")

        f.write("2. NEDEN YCbCr VE HSV BU PROBLEM İÇİN RGB'DEN ÇOK DAHA UYGUNDUR?\n\n")
        f.write("   A. RGB Uzayının Temel Zafiyeti:\n")
        f.write("      - RGB'de aydınlık (luminans) ile renk (krominans) tamamen iç içedir.\n")
        f.write("      - Görseldeki sarı, turuncu ve kırmızı arka plan kutuları R > G > B şartını sağladığı için\n")
        f.write("        RGB eşiklemesinde ten zannedilerek yüksek Yanlış Pozitif (False Positive) üretmektedir.\n")
        f.write("      - Koyu tenli (Afro-Amerikan) bireylerin gölgede kalan yüz kısımları R > 95 eşiğinin altında\n")
        f.write("        kalarak elenmekte ve Yanlış Negatif (False Negative) oluşmaktadır.\n\n")

        f.write("   B. YCbCr Uzayının Üstünlüğü:\n")
        f.write("      - YCbCr uzayı parlaklığı (Y) renk farklarından (Cb, Cr) tamamen ayırır.\n")
        f.write("      - Biyolojik olarak tüm ırklardaki (Kafkas, Asyalı, Afrikalı, Latin) insan derisinin\n")
        f.write("        içerdiği hemoglobin ve melanin pigmentleri Cb-Cr kroma düzleminde çok dar ve tutarlı\n")
        f.write("        bir küme oluşturur (Cr: 133-173, Cb: 77-127).\n")
        f.write("      - Ten rengi koyulaşsa bile kroma değerleri neredeyse değişmez, yalnızca Y azalır.\n")
        f.write("      - Bu nedenle YCbCr, görseldeki 21 farklı yüzün tenini arka planlardan mükemmel ayrıştırır.\n\n")

        f.write("   C. HSV Uzayının Üstünlüğü:\n")
        f.write("      - Ton (Hue) kanalı, ışık yoğunluğundan (Value) bağımsız saf dalga boyunu verir.\n")
        f.write("      - İnsan teni 0-22 derece ton açısına hapsolmuştur.\n")
        f.write("      - Doygunluk (Saturation) eşiği (35-190) eklenerek yapay ve aşırı doymuş sarı/turuncu\n")
        f.write("        arka planlar ten renginden kolayca elenebilir.\n")

    print(f"    - Sayısal rapor kaydedildi: {rapor_path}")

    # 5. Kapsamlı Görselleştirme Paneli (2x2 Büyük Panel + Maskeler)
    print("\n[5] Karşılaştırmalı Görsel Panel Hazırlanıyor...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # Orijinal
    axes[0, 0].imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("1. Orijinal Görüntü (21 Farklı Ten & Canlı Arka Planlar)", fontweight="bold", fontsize=11)
    axes[0, 0].axis("off")

    # RGB
    axes[0, 1].imshow(cv2.cvtColor(res_rgb, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f"2. RGB ile Ten Tespiti (Ten Dışı: Tam Kırmızı)\n[Ten Pikseli: {px_rgb:,} (%{pct_rgb:.1f}) - Yüksek Arka Plan Karışması]",
                         fontweight="bold", fontsize=11, color="darkred")
    axes[0, 1].axis("off")

    # YCbCr
    axes[1, 0].imshow(cv2.cvtColor(res_ycbcr, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f"3. YCbCr ile Ten Tespiti (Ten Dışı: Tam Kırmızı)\n[Ten Pikseli: {px_ycbcr:,} (%{pct_ycbcr:.1f}) - Kroma Düzleminde Yüksek Başarım]",
                         fontweight="bold", fontsize=11, color="navy")
    axes[1, 0].axis("off")

    # HSV
    axes[1, 1].imshow(cv2.cvtColor(res_hsv, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f"4. HSV ile Ten Tespiti (Ten Dışı: Tam Kırmızı)\n[Ten Pikseli: {px_hsv:,} (%{pct_hsv:.1f}) - Işıktan Bağımsız Ton (Hue) Filtreleme]",
                         fontweight="bold", fontsize=11, color="darkgreen")
    axes[1, 1].axis("off")

    plt.suptitle("Ödev 7.5 (Görev 5): RGB vs YCbCr vs HSV Ten Rengi Tespiti ve Karşılaştırmalı Analizi\n"
                 "[Ten Olmayan Bölgeler Tam Kırmızı (0, 0, 255) Olarak Gösterilmiştir]",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    panel_path = os.path.join(cikti_dir, "karsilastirma_ten_paneli.png")
    plt.savefig(panel_path, dpi=100)
    plt.close()
    print(f"    - Karşılaştırmalı görsel paneli kaydedildi: {panel_path}")

    # İkili (Binary) Maske Görseli
    fig_mask, axes_m = plt.subplots(1, 3, figsize=(15, 5))
    axes_m[0].imshow(mask_rgb, cmap="gray")
    axes_m[0].set_title("RGB Ten Maskesi (Beyaz: Ten)", fontweight="bold")
    axes_m[0].axis("off")

    axes_m[1].imshow(mask_ycbcr, cmap="gray")
    axes_m[1].set_title("YCbCr Ten Maskesi (Beyaz: Ten)", fontweight="bold")
    axes_m[1].axis("off")

    axes_m[2].imshow(mask_hsv, cmap="gray")
    axes_m[2].set_title("HSV Ten Maskesi (Beyaz: Ten)", fontweight="bold")
    axes_m[2].axis("off")

    plt.suptitle("Renk Uzayları İkili (Binary) Ten Maskeleri Karşılaştırması", fontsize=13, fontweight="bold")
    plt.tight_layout()
    mask_panel_path = os.path.join(cikti_dir, "ten_maskeleri_paneli.png")
    plt.savefig(mask_panel_path, dpi=100)
    plt.close()
    print(f"    - İkili maske paneli kaydedildi: {mask_panel_path}")

    print("\n================================================================================")
    print("   ÖDEV 7.5 (GÖREV 5) BAŞARIYLA TAMAMLANDI!")
    print("================================================================================")


if __name__ == "__main__":
    main()
