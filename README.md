# Görüntü İşleme ve Bilgisayarlı Görme Ödev Deposu

**Öğrenci:** aliensarsen  
**Ders:** Görüntü İşleme / Bilgisayarlı Görme  
**Depo:** [github.com/aliensarsen/goruntu-isleme](https://github.com/aliensarsen/goruntu-isleme)

---

## 📌 İsimlendirme ve Dizin Formatı
Ödevler hafta hafta ve ödev numarasına göre **`[Hafta].[Ödev]`** formatında yapılandırılmıştır:
- Örnek: **`1.2`** $\rightarrow$ 1. Haftanın 2. Ödevi
- Örnek: **`5.4`** $\rightarrow$ 5. Haftanın 4. Ödevi

---

## 📂 Hafta 5: Renk Kanalları, Histogramlar ve Renk Uzayı Dönüşümleri

| Ödev Kodu | Konu | Çıktılar / Rapor | Bağlantı |
| :---: | :--- | :--- | :---: |
| **5.1** | **Renkli Görüntü Kanal Histogramları ve Siyah-Beyaz Dönüşümü**<br>• Mavi, Yeşil, Kırmızı kanalları ayrı histogram analizi<br>• Gri seviye (Grayscale) ve ikili siyah-beyaz (Otsu & Fixed Threshold) | `output_grayscale.jpg`<br>`output_binary_otsu.jpg`<br>`histogram_analiz_sonucu.png` | [📂 İncele](Hafta_5/5.1/) |
| **5.2** | **Özel `calcHist` Fonksiyonu ve Kanal Histogramları**<br>• `cv2.calcHist()` kullanılmadan sıfırdan histogram fonksiyonu<br>• Her kanal için ayrı ayrı hesaplama ve OpenCV doğrulama (Fark = 0.0) | `custom_calc_hist()`<br>`custom_histogram_grafikleri.png` | [📂 İncele](Hafta_5/5.2/) |
| **5.3** | **Özel Gri Dönüşüm ve OpenCV Mutlak Hata Analizi**<br>• ITU-R BT.601 standardı ile `custom_bgr2gray()` formülü ($Y = 0.299R + 0.587G + 0.114B$)<br>• OpenCV `cv2.cvtColor()` ile piksel mutlak farkı (SAD = 7, %99.99 Eşleşme) | `output_gray_opencv.jpg`<br>`output_gray_custom.jpg`<br>`gri_donusum_ve_hata_analizi.png` | [📂 İncele](Hafta_5/5.3/) |
| **5.4** | **Renk Uzayı Dönüşümleri, Fonksiyon Göstericileri & Hata Doğrulaması**<br>• BGR $\leftrightarrow$ RGB, RGBA, BGRA, Grayscale<br>• Python First-Class Functions / Dispatch Table mimarisi<br>• OpenCV ile sayısal doğrulama (Beklenen Hata: 0, BGR/RGB/RGBA/BGRA = 0.0) | `main.py`<br>`main.cpp` (Bonus C++)<br>`karsilastirma_ve_hata_paneli.png` | [📂 İncele](Hafta_5/5.4/) |
| **5.5** | **X-Ray Görüntülerinde Sahte Renklendirme ve Güvenlik Paleti Analizi**<br>• HUMS X-Ray veri setinden 5 adet tehdit görselinin griye dönüştürülmesi<br>• Havalimanı standardı 3-renk (Dual-Energy Material) sahte renklendirme (LUT)<br>• Çift enerji fiziksel bilgi kaybı analizi, PSNR/MSE metrikleri ve öz eleştiri | `main.py`<br>`tum_gorseller_renklendirme_paneli.png`<br>`outputs/` | [📂 İncele](Hafta_5/5.5/) |

---

## 🛠️ Genel Gereksinimler ve Çalıştırma
```bash
pip install opencv-python numpy matplotlib
```
Herhangi bir ödevi çalıştırmak için ilgili klasöre gidip `main.py` dosyasını çalıştırmanız yeterlidir:
```bash
cd Hafta_5/5.1 && python3 main.py
cd Hafta_5/5.2 && python3 main.py
cd Hafta_5/5.3 && python3 main.py
cd Hafta_5/5.4 && python3 main.py
cd Hafta_5/5.5 && python3 main.py
```
*(Tüm betikler resim parametresi verilmediğinde sentetik renkli bir görsel üretip otomatik olarak testleri tamamlar).*
