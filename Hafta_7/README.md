# 📂 Hafta 7: Renk Uzayları, Görüntü Formatları ve Dönüşüm Analizi

Bu klasör, Görüntü İşleme dersinin 7. haftasına ait tüm laboratuvar ve uygulama ödevlerini içerir.

| Ödev Kodu | Görev Tanımı | Betik | Çıktılar / Rapor |
| :---: | :--- | :--- | :--- |
| **7.1** | **Görev 1: Renk Uzayları Araştırması**<br>• RGB, HSV, YUV, CIE L\*a\*b\*, Grayscale, CMYK kuramsal incelemesi<br>• Model türleri, avantaj ve dezavantajları, problem türlerine göre seçim kriterleri | [`README.md`](7.1/README.md) | `cikti/renk_uzaylari_karsilastirma.png`<br>`README.md` |
| **7.2** | **Görev 2: 1000x1000 BMP Boyut ve Kanal Analizi**<br>• $1000 \times 1000$ 24-bit renkli BMP $\rightarrow$ 8-bit gri seviye BMP dönüşümü<br>• DIB/BMP başlıkları, 1024 baytlık renk paleti ve kanal sayısı kıyaslaması ($3{,}000{,}054$ vs $1{,}001{,}078$ bayt) | [`main.py`](7.2/main.py)<br>[`README.md`](7.2/README.md) | `cikti/gri_1000x1000.bmp`<br>`cikti/boyut_analizi_raporu.txt`<br>`cikti/karsilastirma_gorsel.png` |
| **7.3** | **Görev 3: 8K BMP Düzenleme ve Hassas Süre Ölçümü**<br>• 8K UHD ($7680 \times 4320 \times 3$) 24-bit BMP görüntüsü ($99{,}532{,}854$ bayt)<br>• OpenCV ile açma; piksel değerlerini 2'ye bölme (`img // 2`, `>> 1`, in-place, `cv2.divide`, threading)<br>• Dosya açma/kaydetme hariç yalnız düzenleme süresi (8.67 ms / 10.69 GB/sn) | [`main.py`](7.3/main.py)<br>[`README.md`](7.3/README.md) | `cikti/8k_duzenlenmis.bmp`<br>`cikti/sure_ve_performans_raporu.txt`<br>`cikti/8k_karsilastirma_ve_sure.png`<br>`cikti/8k_onizleme_*.jpg` |
| **7.4** | **Görev 4: Renk Uzayları Dönüşümü (HSV, HSI, YUV, CIE Lab) ve BMP Kaydetme**<br>• RGB BMP görüntüsünün HSV, HSI, YUV, CIE L\*a\*b\* uzaylarına dönüştürülmesi<br>• Sıfırdan Gonzalez & Woods formülüyle HSI fonksiyonu ($I = (R+G+B)/3$)<br>• Her bir uzayın 3-kanallı 24-bit BMP olarak kaydedilmesi ve 5x4 ızgara paneli | [`main.py`](7.4/main.py)<br>[`README.md`](7.4/README.md) | `cikti/resim_hsv.bmp`<br>`cikti/resim_hsi.bmp`<br>`cikti/resim_yuv.bmp`<br>`cikti/resim_cielab.bmp`<br>`cikti/renk_uzaylari_paneli.png`<br>`cikti/donusum_raporu.txt` |
| **7.5** | **Görev 5: Ten Rengi Tespiti (RGB, YCbCr, HSV) ve Ten Dışı Tam Kırmızı Gösterme**<br>• 21 farklı etnik yüze sahip görüntüde ten rengi segmentasyonu<br>• RGB (Peer et al.), YCbCr (Chai & Ngan) ve HSV kuralları<br>• Ten olmayan tüm piksellerin tam kırmızı `[0, 0, 255]` yapılması ve karşılaştırmalı paneli | [`main.py`](7.5/main.py)<br>[`README.md`](7.5/README.md) | `cikti/ten_rgb.png`<br>`cikti/ten_ycbcr.png`<br>`cikti/ten_hsv.png`<br>`cikti/karsilastirma_ten_paneli.png`<br>`cikti/ten_maskeleri_paneli.png`<br>`cikti/ten_tespiti_raporu.txt` |
| **7.6** | **Görev 6: Video/Webcam Hareketli Bölge Tespiti (ROI) ve Ten Rengi Renklendirme**<br>• Video akışı / kamera çerçeve farkı ($|G_t - G_{t-1}| > 20$, adaptif hareket eşiği $>1200\text{ px}$)<br>• Hareketli ROI tespiti ve arka planı karartma (%45 aydınlık)<br>• Sadece hareketli ROI içinde YCbCr & HSV ten tespiti ve yarı saydam yeşil renklendirme | [`main.py`](7.6/main.py)<br>[`README.md`](7.6/README.md) | `cikti/hareket_ve_ten_tespiti.png`<br>`cikti/hareket_ve_ten_paneli.png`<br>`cikti/hareket_ve_ten_raporu.txt` |
| **7.7** | **Görev 7: Trafik İşaretlerinde Kırmızı Çember Tespiti (Kaggle GTSRB Veri Seti)**<br>• Kaggle GTSRB trafik işaretleri kıyaslaması (Hız 50, 30, Geçiş Yasağı, Üçgen, Dikdörtgen)<br>• Çoklu renk uzayı kırmızı segmentasyonu (HSV, YCbCr, CIE L\*a\*b\*) hibrit füzyonu<br>• `cv2.HoughCircles` çember tespiti ve dairesellik ($\ge 0.70$) geometrik doğrulaması | [`main.py`](7.7/main.py)<br>[`README.md`](7.7/README.md) | `cikti/trafik_tabelalari_tespit_paneli.png`<br>`cikti/renk_uzaylari_kirmizi_maske_paneli.png`<br>`cikti/hough_tespit_raporu.txt` |

---

## 🚀 Hızlı Başlangıç

```bash
# 7.2 Ödevi (1000x1000 BMP ve Boyut Analizi):
cd Hafta_7/7.2 && python3 main.py

# 7.3 Ödevi (8K Düzenleme ve Süre Ölçümü):
cd Hafta_7/7.3 && python3 main.py

# 7.4 Ödevi (HSV, HSI, YUV, CIE Lab BMP Dönüşümleri):
cd Hafta_7/7.4 && python3 main.py

# 7.5 Ödevi (Ten Rengi Tespiti ve Ten Dışı Tam Kırmızı):
cd Hafta_7/7.5 && python3 main.py

# 7.6 Ödevi (Webcam / Video Hareketli ROI ve Ten Tespiti):
cd Hafta_7/7.6 && python3 main.py
# (Gerçek kamera için: python3 main.py --webcam)

# 7.7 Ödevi (Kaggle Trafik İşaretleri Kırmızı Çember Tespiti):
cd Hafta_7/7.7 && python3 main.py
```
