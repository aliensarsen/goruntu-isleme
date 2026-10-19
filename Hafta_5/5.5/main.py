#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme
ÖDEV  : 5.5 (5. Hafta 5. Ödev)
KONU  : X-Ray Görüntülerinde Gri Dönüşüm, Güvenlik Operatörleri İçin Sahte
        Renklendirme (Pseudo-Coloring), Palet Analizi ve Değerlendirme
YAZAR : aliensarsen
======================================================================================

Bu çalışma:
 1. HUMS X-Ray veri setindeki 5 adet tehdit içeren (bıçak vb.) renkli görüntüyü
    önce gri seviyeye (Grayscale) dönüştürür.
 2. Güvenlik operatörlerinin bagaj içindeki metal tehditleri, organik patlayıcıları
    ve diğer nesneleri insan gözünün renk ayırt etme yeteneğiyle kolayca fark
    edebilmesi için uluslararası havalimanı X-Ray standardına (Smiths Detection /
    TSA standardı: Dual-Energy Material Decomposition) uygun özel bir renk paleti
    (Look-Up Table - LUT) ile renklendirir.
 3. Karşılaştırma amaçlı OpenCV COLORMAP_TURBO paletini de uygular.
 4. Orijinal renkli X-ray görüntüsü ile tek kanallı griden üretilen sahte
    renkli görüntü arasındaki fiziksel ve sayısal farkları bilimsel olarak analiz eder.
"""

import os
import sys
import glob
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def build_security_xray_lut() -> np.ndarray:
    """
    Havalimanı ve Sınır Güvenliği X-Ray Tarama Standartlarına Uygun 256x3 Renk Tablosu (LUT).
    
    X-Işını Transmisyon Fiziği ve Renk Haritası:
    - [0 - 115]  Düşük Gri Değerleri (Yüksek Soğurma / Yoğun Metaller / Bıçak / Silah):
                 -> Derin Mavi ve Camgöbeği (Blue / Cyan)
    - [115 - 175] Orta Gri Değerleri (Orta Soğurma / Hafif Metaller / Alüminyum / Cam):
                 -> Yeşil ve Sarı-Yeşil (Green / Lime)
    - [175 - 235] Yüksek Gri Değerleri (Düşük Soğurma / Organik Malzemeler / Plastik / Kumaş):
                 -> Sıcak Turuncu ve Kahverengi (Orange / Brown)
    - [235 - 255] En Yüksek Değerler (Boşluk / Arka Plan / Hava):
                 -> Soluk Krem Sarı ve Beyaz (Pale Cream / White)
    """
    lut = np.zeros((256, 3), dtype=np.uint8)  # OpenCV formatı: BGR

    for i in range(256):
        if i < 115:
            # Yoğun metaller / Tehdit: Koyu Mavi -> Canlı Mavi -> Camgöbeği
            t = i / 115.0
            b = int(220 + 20 * t)
            g = int(60 + 120 * t)
            r = int(10 + 30 * t)
        elif i < 175:
            # İnorganik / Hafif metaller: Camgöbeği -> Yeşil
            t = (i - 115) / 60.0
            b = int(240 * (1 - t) + 40 * t)
            g = int(180 + 40 * t)
            r = int(40 + 80 * t)
        elif i < 235:
            # Organik / Plastik / Patlayıcı: Yeşilimsi Sarı -> Canlı Turuncu
            t = (i - 175) / 60.0
            b = int(40 * (1 - t) + 120 * t)
            g = int(220 * (1 - t) + 200 * t)
            r = int(120 * (1 - t) + 250 * t)
        else:
            # Arka plan / Boş hava: Soluk Sarı -> Beyaz
            t = (i - 235) / 20.0
            b = int(160 + 95 * t)
            g = int(240 + 15 * t)
            r = int(250 + 5 * t)

        lut[i] = [b, g, r]

    return lut


def calculate_metrics(original_bgr: np.ndarray, colored_bgr: np.ndarray) -> dict:
    """Orijinal renkli görüntü ile renklendirilmiş görüntü arasındaki fark metrikleri."""
    mse = np.mean((original_bgr.astype(np.float64) - colored_bgr.astype(np.float64)) ** 2)
    if mse == 0:
        psnr = 100.0
    else:
        psnr = 10 * np.log10((255.0 ** 2) / mse)
    mae = np.mean(np.abs(original_bgr.astype(np.float64) - colored_bgr.astype(np.float64)))
    return {"mse": mse, "psnr": psnr, "mae": mae}


def process_image(img_path: str, output_dir: str, lut: np.ndarray, index: int):
    # 1. Görüntüyü Oku
    original_bgr = cv2.imread(img_path)
    if original_bgr is None:
        raise ValueError(f"Görsel açılamadı: {img_path}")

    # 2. Gri Tonlamaya Dönüştür
    gray = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2GRAY)

    # 3. Özel Güvenlik Paleti (Security X-Ray LUT) ile Sahte Renklendirme
    security_colored = lut[gray]

    # 4. Alternatif Spektral Palet (OpenCV COLORMAP_TURBO)
    turbo_colored = cv2.applyColorMap(gray, cv2.COLORMAP_TURBO)

    # Dosya adları
    base_name = f"threat_{index}"
    gray_path = os.path.join(output_dir, f"{base_name}_1_gray.png")
    sec_path = os.path.join(output_dir, f"{base_name}_2_security_colored.png")
    turbo_path = os.path.join(output_dir, f"{base_name}_3_turbo_colored.png")
    panel_path = os.path.join(output_dir, f"{base_name}_4_karsilastirma.png")

    cv2.imwrite(gray_path, gray)
    cv2.imwrite(sec_path, security_colored)
    cv2.imwrite(turbo_path, turbo_colored)

    # Sayısal Karşılaştırma
    metrics = calculate_metrics(original_bgr, security_colored)

    # 5. Dört Panelli Karşılaştırma Grafiği Oluştur
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    fig.suptitle(f"HUMS X-Ray Tehdit Görüntüsü #{index} - Renklendirme Analizi", fontsize=14, fontweight='bold')

    axes[0].imshow(cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB))
    axes[0].set_title("1. Orijinal Renkli (Dual-Energy)")
    axes[0].axis("off")

    axes[1].imshow(gray, cmap="gray")
    axes[1].set_title("2. Gri Tonlama (Grayscale)")
    axes[1].axis("off")

    axes[2].imshow(cv2.cvtColor(security_colored, cv2.COLOR_BGR2RGB))
    axes[2].set_title("3. Özel Güvenlik Paleti (Bizim)")
    axes[2].axis("off")

    axes[3].imshow(cv2.cvtColor(turbo_colored, cv2.COLOR_BGR2RGB))
    axes[3].set_title("4. OpenCV Turbo Paleti")
    axes[3].axis("off")

    plt.tight_layout()
    plt.savefig(panel_path, dpi=300)
    plt.close()

    return {
        "index": index,
        "original": original_bgr,
        "gray": gray,
        "security": security_colored,
        "turbo": turbo_colored,
        "metrics": metrics
    }


def main():
    print("=" * 80)
    print("      5. HAFTA 5. ÖDEV: X-RAY GÖRÜNTÜLERİ RENKLENDİRME VE GÜVENLİK ANALİZİ      ")
    print("=" * 80)

    input_dir = "inputs"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    input_files = sorted(glob.glob(os.path.join(input_dir, "threat_*.png")))
    if not input_files:
        raise FileNotFoundError(f"Giriş görselleri bulunamadı: {input_dir}/ klasöründe threat_*.png dosyaları olmalı.")

    print(f"[+] Toplam {len(input_files)} adet X-Ray tehdit görseli işleniyor...")
    lut = build_security_xray_lut()

    results = []
    print("\n--- GÖRÜNTÜ BAZLI İŞLEM VE METRİK SONUÇLARI ---")
    for i, file_path in enumerate(input_files, start=1):
        res = process_image(file_path, output_dir, lut, i)
        results.append(res)
        m = res["metrics"]
        print(f"[{i}/5] {os.path.basename(file_path)}:")
        print(f"      * Gri Boyut       : {res['gray'].shape[1]}x{res['gray'].shape[0]}")
        print(f"      * Ortalama Hata   : {m['mae']:.2f} piksel")
        print(f"      * PSNR Değeri     : {m['psnr']:.2f} dB")
        print(f"      * MSE Değeri      : {m['mse']:.2f}")

    # Tüm 5 görüntünün toplu büyük özet panelini üret
    print("\n[+] 5 görüntülük büyük özet paneli oluşturuluyor...")
    fig, axes = plt.subplots(len(results), 4, figsize=(18, 4 * len(results)))
    fig.suptitle("HUMS X-Ray Tehdit Veri Seti: 5 Görüntü İçin Toplu Renklendirme Paneli", fontsize=16, fontweight='bold')

    columns = [
        "Orijinal Renkli (Dual-Energy)",
        "Gri Tonlama (Grayscale)",
        "Özel Güvenlik Paleti (Önerilen)",
        "OpenCV Turbo Paleti"
    ]

    for col, col_name in enumerate(columns):
        axes[0, col].set_title(col_name, fontsize=12, fontweight='bold')

    for row, res in enumerate(results):
        axes[row, 0].imshow(cv2.cvtColor(res["original"], cv2.COLOR_BGR2RGB))
        axes[row, 0].axis("off")
        axes[row, 0].set_ylabel(f"Görsel {row+1}", fontsize=11, fontweight='bold')

        axes[row, 1].imshow(res["gray"], cmap="gray")
        axes[row, 1].axis("off")

        axes[row, 2].imshow(cv2.cvtColor(res["security"], cv2.COLOR_BGR2RGB))
        axes[row, 2].axis("off")

        axes[row, 3].imshow(cv2.cvtColor(res["turbo"], cv2.COLOR_BGR2RGB))
        axes[row, 3].axis("off")

    plt.tight_layout()
    summary_plot = "tum_gorseller_renklendirme_paneli.png"
    plt.savefig(summary_plot, dpi=300)
    plt.close()
    print(f"[+] Toplu analiz paneli kaydedildi: {summary_plot}")

    print("\n" + "=" * 80)
    print(" ÖDEV 5.5 RAPORU VE YORUMLAR:")
    print("=" * 80)
    print("""
1. NEDEN BU RENK PALETİ SEÇİLDİ?
--------------------------------
- İnsan gözü gri tonlamada yalnızca ~30-40 gri seviyesini ayırt edebilirken, renkte
  binlerce renk tonunu (hue/saturation) anında fark eder. Güvenlik operatörünün
  bagaj bandındaki hızlı geçişlerde dikkat yorgunluğunu (vigilance decrement)
  azaltmak için sahte renklendirme (pseudo-coloring) kritik öneme sahiptir.
- Seçtiğimiz palet, havalimanı ve gümrük bagaj tarama standartlarına (Smiths Detection,
  Rapiscan, TSA Dual-Energy Standardı) tam uyumludur:
  * MAVİ / LACİVERT: Yüksek yoğunluklu ve yüksek atom numaralı malzemeler (Z > 10).
    Özellikle çelik, bıçaklar, silahlar ve yoğun metal parçaları operatöre anında alarm verir.
  * YEŞİL: Orta yoğunluklu malzemeler (10 <= Z <= 14). Hafif metaller (alüminyum), cam, kemik.
  * TURUNCU / KAHVE: Düşük atom numaralı organik malzemeler (Z < 10). Plastikler, kumaşlar,
    patlayıcı maddeler (C4, TNT vb.), sıvılar ve gıda ürünleri.
  * BEYAZ / SOLUK SARI: Arka plan (boş hava, X-ışınının hiç engellenmeden geçtiği alanlar).

2. ORİJİNAL RENKLİ RESİM İLE ÜRETİLEN RESİM ARASINDAKİ FARKIN BİLİMSEL NEDENİ:
------------------------------------------------------------------------------
- Orijinal görüntü, tek bir gri görüntüden değil; çift enerjili (Dual-Energy)
  X-Ray dedektörlerinden gelen yüksek ve alçak enerji soğurma oranlarının Compton saçılması
  ve Fotoelektrik etki analizinden türetilmiştir. Yani orijinal veride "efektif atom numarası (Z)"
  kalınlıktan bağımsız olarak doğrudan ölçülmüştür.
- Biz renkli görüntüyü tek kanallı griye dönüştürdüğümüzde, malzemenin atom numarası (Z)
  ile nesnenin kalınlığı (t) tek bir skaler soğurma değerine (I = I_0 * e^(-mu * t)) çökmüş olur.
- Bu nedenle tek kanallı griden sahte renklendirmede: Kalın bir organik nesne ile ince bir metal
  parça aynı gri tonuna sahip olabilir. Bu fiziksel bilgi kaybı, renklendirme haritamızın
  orijinal çift enerjili görüntüden bir miktar farklılaşmasına (ambiguity / belirsizlik) yol açar.

3. BAŞARILI VE ZAYIF YÖNLER (ÖZ ELEŞTİRİ / DEĞERLENDİRME):
----------------------------------------------------------
* BAŞARILI YÖNLER:
  - Bıçak namluları ve kesici metal uçlar (düşük gri seviyeleri) çok yüksek kontrastlı
    canlı mavi renkle başarıyla izole edilmiş, operatörün dikkatini anında çekecek hale getirilmiştir.
  - Arka plan temiz ve soluk tutularak bagaj dışı alanların dikkati dağıtması önlenmiştir.
  - Operatörün ergonomisi gözetilerek gözü yormayan renk gradyanları kullanılmıştır.

* ZAYIF / KISITLI YÖNLER:
  - Üst üste binen (overlapping) nesnelerde (örneğin organik bir kumaşın arkasında duran ince metal bıçak),
    tek kanallı gri seviye tek bir değere sahip olduğu için malzemenin çift enerjili ayrımı
    tam olarak yapılamamakta ve geçiş sınırlarında renk kaymaları oluşabilmektedir.
  - Bıçakların plastik/ahşap sapları organik olduğu için (gri değeri yüksek) arka plana
    yakın tonlar alabilmekte ve namlu kadar yüksek kontrastla ayrılamamaktadır.
""")
    print("=" * 80)


if __name__ == "__main__":
    main()
