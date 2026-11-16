# Ödev 7.1 (Görev 1): Renk Uzayları Araştırması ve Karşılaştırmalı Analiz

Bu çalışma, görüntü işleme alanında yaygın kullanılan temel renk uzaylarının (RGB, HSV, YUV, CIE L\*a\*b\*, Grayscale, CMYK) matematiksel temellerini, insan algısıyla ilişkilerini, avantaj ve dezavantajlarını ve hangi problemler için hangi renk uzayının tercih edilmesi gerektiğini kapsamlı bir şekilde araştırmaktadır.

---

## 1. Görüntü İşlemede Yaygın Renk Uzayları

Görüntü işlemede evrensel tek bir renk uzayı yoktur. Donanım aygıtları (kameralar, ekranlar, yazıcılar), insan görme sistemi ve matematiksel algoritmalar farklı renk gösterimleri gerektirir.

### 1.1. Renk Uzaylarının Kapsamlı Karşılaştırması

| Renk Uzayı | Kanallar / Bileşenler | Model Türü | Başlıca Avantajları | Başlıca Dezavantajları | Tercih Edilen Problem ve Alanlar |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RGB / BGR** | **R:** Kırmızı (Red)<br>**G:** Yeşil (Green)<br>**B:** Mavi (Blue) | Toplamsal (Additive)<br>Donanım Tabanlı | • Ekran (LCD/OLED) ve kamera sensörlerine (Bayer filtresi) doğrudan 1:1 eşlenir.<br>• Doğal ve anlaşılması kolay kartezyen küp modelidir. | • **Aydınlık (Luminans) ile Renk (Krominans) birbirinden ayrılamaz.**<br>• Ortam ışığı veya gölge değiştiğinde 3 kanalın değeri de radikal değişir.<br>• Kanallar arası korelasyon çok yüksektir ($r > 0.85$). | • Ham görüntü yakalama (kamera/tarayıcı sensörleri)<br>• Web ve ekran monitör gösterimi<br>• Ham piksel depolama |
| **HSV / HSL** | **H:** Ton (Hue, 0-360°)<br>**S:** Doygunluk (Saturation)<br>**V / L:** Değer/Parlaklık (Value/Lightness) | Silindirik / Açısal<br>İnsan Algısına Yakın | • **Işık Değişimlerine Dayanıklılık:** Aydınlık (V), renkten (H, S) tamamen ayrılmıştır.<br>• Gölgeler ve ışık parlamaları altında nesne rengi (H) neredeyse sabit kalır.<br>• Eşikleme ile renk filtreleme çok kolaydır. | • Sıfır doygunlukta ($S \approx 0$) veya karanlıkta ($V \approx 0$) açısal Ton (H) belirsizleşir (matematiksel tekillik).<br>• Ton açısı 0° ile 360° arasında daireseldir (kırmızı hem 0° hem 360°'de yer alır). | • **Renk tabanlı nesne takibi** (top, şerit, robot takibi)<br>• Cilt rengi (skin color) segmentasyonu<br>• Grafik programlarında renk seçim paletleri (color picker) |
| **YUV / YCbCr** | **Y:** Aydınlık (Luma)<br>**U / Cb:** Mavi Renk Farkı<br>**V / Cr:** Kırmızı Renk Farkı | Ayrık Luma + Kroma<br>Yayın ve Sıkıştırma | • İnsan gözü renge kıyasla aydınlık detayına çok daha duyarlıdır. **Kroma Alt Örnekleme (Chroma Subsampling: 4:2:0)** ile renk çözünürlüğü yarıya indirilip dosya boyutu %50-%75 azaltılır.<br>• Siyah-beyaz sistemlerle geriye dönük tam uyumludur ($Y$ kanalı tek başına gri görüntüdür). | • İnsan zihni için sezgisel değildir (U ve V negatif ve pozitif fark eksenleridir).<br>• Matris dönüşümlerinde katsayılar ve yuvarlama hataları oluşabilir. | • **Video sıkıştırma ve aktarımı** (H.264, H.265/HEVC, AV1, MP4)<br>• Televizyon yayıncılığı (PAL, NTSC)<br>• JPEG fotoğraf sıkıştırma formatı |
| **CIE L\*a\*b\*** | **L\*:** Algısal Aydınlık (0-100)<br>**a\*:** Yeşil $\leftrightarrow$ Kırmızı<br>**b\*:** Mavi $\leftrightarrow$ Sarı | Algısal Olarak Düzgün<br>(Perceptually Uniform)<br>Cihazdan Bağımsız | • **Algısal Düzgünlük:** Uzaydaki Öklid mesafesi ($\Delta E = \sqrt{\Delta L^2 + \Delta a^2 + \Delta b^2}$), insan gözünün hissettiği farkla tam örtüşür.<br>• Cihazdan bağımsızdır (monitör veya yazıcı profillerine bağlı kalmaz). | • Matematiksel dönüşümü ağırdır (XYZ ara uzayı, küpkök ve standart beyaz referans noktası $D_{65}$ gerektirir).<br>• Koordinatlar elle ayarlama için sezgisel değildir. | • **Endüstriyel renk kalite kontrolü** (tekstil, otomotiv boya toleransı, plastik kalıplama)<br>• Delta E ($\Delta E$) hata ölçümleri<br>• Fotoğraflar arası renk transferi algoritmaları |
| **Grayscale** | **Y / L:** Tek Kanallı Yoğunluk (0-255) | Tek Boyutlu Luma | • Bellek ve disk boyutunu RGB'ye kıyasla 3 kat azaltır.<br>• Hesaplama karmaşıklığını ve işlemci süresini radikal ölçüde düşürür.<br>• Kromatik gürültüyü yok eder; gradyan, doku ve kenar algılamayı basitleştirir. | • Tüm renk bilgisini kaybeder.<br>• Farklı renkte fakat aynı parlaklık değerine sahip pikseller (örneğin saf yeşil ile saf kırmızı) gri seviyede ayırt edilemez. | • Kenar tespiti (Sobel, Canny, Prewitt, LoG)<br>• Öznitelik çıkarımı (SIFT, SURF, ORB, Harris Köşe)<br>• Optik Karakter Tanıma (OCR), morfolojik işlemler<br>• Tıbbi görüntüleme (Röntgen / X-Ray, BT, MR) |
| **CMYK** | **C:** Camgöbeği (Cyan)<br>**M:** Galibarda (Magenta)<br>**Y:** Sarı (Yellow)<br>**K:** Siyah (Key / Black) | Çıkarmalı (Subtractive)<br>Fiziksel Baskı Tabanlı | • Baskı mürekkeplerinin kağıt üzerindeki ışık soğurma fiziğiyle doğrudan örtüşür.<br>• Ayrı bir siyah mürekkep (K) kullanımı renk karışımından daha net siyah verir ve maliyeti düşürür. | • Dijital ekranlar için kullanılamaz.<br>• Renk gamutu RGB'den daha dardır (ekrandaki bazı parlak/canlı renkler kağıda basılamaz). | • Matbaacılık, ofset baskı, profesyonel masaüstü yazıcılar<br>• Yayıncılık baskı öncesi (prepress) hazırlığı |

---

## 2. Problem Türlerine Göre Renk Uzayı Seçim Kriterleri

1. **Gölge ve Işık Değişimi Altında Renk Takibi Yapılacaksa:**
   - **Tercih:** **HSV** veya **HSI**.
   - **Gerekçe:** Işık şiddeti $V$ (Value) veya $I$ (Intensity) kanalında izole edilmiştir. Ortam aydınlığı veya gölgeler değişse bile Ton ($H$) neredeyse sabit kalır.
2. **Video Sıkıştırma ve Ağ Üzerinden Aktarım Yapılacaksa:**
   - **Tercih:** **YUV** veya **YCbCr**.
   - **Gerekçe:** İnsan gözü renge kıyasla aydınlık detaylarına çok daha duyarlıdır. $Y$ kanalı tam çözünürlükte tutulurken, renk farkı kanalları ($Cb, Cr$) 4:2:0 oranında yarıya indirilerek bant genişliği %50-%75 korunur.
3. **Endüstriyel Üretimde Renk Tutarlılığı Ölçülecekse:**
   - **Tercih:** **CIE L\*a\*b\***.
   - **Gerekçe:** CIE Lab, insan gözünün renk ayırt etme eşiğine (JND - Just Noticeable Difference) göre tasarlanmış algısal olarak düzgün (perceptually uniform) bir uzaydır. $\Delta E$ formülü ile iki renk arasındaki fark tam olarak insan algısına göre derecelendirilir.
4. **Kenar Tespiti, Doku Analizi veya Şekil Tanıma Yapılacaksa:**
   - **Tercih:** **Grayscale**.
   - **Gerekçe:** Renk bilgisi kenar gradyanlarını ve köşe noktalarını tespit etmek için gereksiz veri fazlalığı (redundancy) yaratır. Tek kanala düşmek hesaplama hızını 3 kat artırır.

---

## 3. Görsel Karşılaştırma

`cikti/renk_uzaylari_karsilastirma.png` görselinde RGB, HSV, YUV ve CIE Lab uzaylarının 12 alt kanala ayrılmış haritası incelenebilir.
