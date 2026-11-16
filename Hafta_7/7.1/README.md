# Ödev 7.1: Renk Uzayları Araştırması ve 1000x1000 BMP Dosya Boyutu / Kanal Analizi

Bu çalışma, görüntü işlemede yaygın kullanılan temel renk uzaylarının (RGB, HSV, YUV, CIE L\*a\*b\*, Grayscale, CMYK) kuramsal ve pratik özelliklerini, avantaj/dezavantajlarını ve kullanım alanlarını kapsamlı biçimde araştırmakta; ayrıca $1000 \times 1000$ boyutundaki 24-bit renkli ve 8-bit gri seviye BMP (Bitmap) formatındaki görüntülerin disk ayak izlerini çözünürlük, kanal sayısı ve ikili (binary) dosya başlık yapısı düzeyinde incelemektedir.

---

## 1. Görüntü İşlemede Yaygın Renk Uzayları Araştırması

Görüntü işleme uygulamalarında tek bir evrensel renk modeli bulunmaz. Donanım aygıtları (kameralar, ekranlar, yazıcılar), insan algısı ve matematiksel/istatistiksel modeller farklı renk gösterimleri gerektirir.

### 1.1. Renk Uzaylarının Kapsamlı Karşılaştırması

| Renk Uzayı | Bileşenler / Kanallar | Model Türü | Başlıca Avantajları | Başlıca Dezavantajları | Tercih Edilen Problem / Alanlar |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RGB / BGR** | **R:** Kırmızı (Red)<br>**G:** Yeşil (Green)<br>**B:** Mavi (Blue) | Toplamsal (Additive)<br>Donanım Tabanlı | • Ekran (LCD/OLED) ve kamera (Bayer sensör) donanımlarına doğrudan birebir eşlenir.<br>• Doğal ve anlaşılması kolay kartezyen küp modelidir. | • Renk (krominans) ile aydınlık (luminans) birbirinden ayrılamaz.<br>• Işık şiddeti değiştiğinde üç kanal da radikal değişir (gölge ve aydınlatma hassasiyeti yüksektir).<br>• Kanallar arası korelasyon çok yüksektir ($r > 0.85$). | • Ham görüntü yakalama (kamera sensörleri)<br>• Web ve ekran monitör gösterimi<br>• Ham piksel depolama formatları |
| **HSV / HSL** | **H:** Ton (Hue, 0-360°)<br>**S:** Doygunluk (Saturation)<br>**V / L:** Değer/Aydınlık (Value/Lightness) | Silindirik / Açısal<br>İnsan Algısına Yakın | • **Işık Değişimlerine Dayanıklılık:** Aydınlık (V), renkten (H, S) tamamen ayrılmıştır.<br>• Gölgeler ve ışık parlamaları altında nesne rengi (H) neredeyse sabit kalır.<br>• Eşikleme ile renk filtreleme çok kolaydır. | • Sıfır doygunlukta ($S \approx 0$) veya karanlıkta ($V \approx 0$) açısal Ton (H) belirsizleşir (matematiksel tekillik / singularity).<br>• Ton açısı 0° ile 360° arasında daireseldir (kırmızı hem 0° hem 360°'de yer alır; OpenCV'de [0, 10] ve [170, 180] aralığı). | • Renk tabanlı nesne takibi (top, araç, şerit takibi)<br>• Cilt rengi (skin color) segmentasyonu<br>• Grafik programlarında renk seçim paletleri (color picker) |
| **YUV / YCbCr** | **Y:** Aydınlık (Luma)<br>**U / Cb:** Mavi Renk Farkı<br>**V / Cr:** Kırmızı Renk Farkı | Ayrık Luma + Kroma<br>Yayın ve Sıkıştırma | • İnsan gözünün aydınlığa (detaya) duyarlı, renge daha az duyarlı olmasından faydalanarak **Kroma Alt Örnekleme (Chroma Subsampling: 4:2:0, 4:2:2)** ile bant genişliğini ve dosya boyutunu %50-%75 azaltır.<br>• Siyah-beyaz ekranlarla geriye dönük tam uyumludur ($Y$ kanalı tek başına gri seviyedir). | • İnsan zihni için sezgisel değildir (U ve V negatif ve pozitif fark eksenleridir).<br>• Dönüşümlerde matris katsayıları ve yuvarlama hataları oluşabilir. | • Video sıkıştırma standartları (H.264, H.265/HEVC, AV1, VP9)<br>• Televizyon yayıncılığı (PAL, NTSC)<br>• JPEG fotoğraf sıkıştırma standardı |
| **CIE L\*a\*b\*** | **L\*:** Algısal Aydınlık (0-100)<br>**a\*:** Yeşil $\leftrightarrow$ Kırmızı (-128, +127)<br>**b\*:** Mavi $\leftrightarrow$ Sarı (-128, +127) | Algısal Olarak Düzgün<br>(Perceptually Uniform)<br>Cihazdan Bağımsız | • **Algısal Düzgünlük:** Uzaydaki Öklid mesafesi ($\Delta E = \sqrt{\Delta L^{*2} + \Delta a^{*2} + \Delta b^{*2}}$), insan gözünün hissettiği renk farkına tam olarak orantılıdır.<br>• Cihaz bağımsızdır (monitör veya yazıcı profillerine bağlı kalmaz). | • Matematiksel dönüşümü ağırdır (XYZ ara uzayı, küpkök ve beyaz nokta referansı $D_{65}$ gerektirir).<br>• Piksel değerleri doğrudan sezgisel anlaşılamaz. | • Endüstriyel renk kalite kontrolü (tekstil, otomotiv boyası, plastik)<br>• Delta E ($\Delta E$) renk farkı tolerans testleri<br>• Fotoğraf renk aktarımı (color transfer) algoritmaları |
| **Grayscale** | **Y / L:** Tek Kanallı Yoğunluk (0-255) | Tek Boyutlu Luma | • Bellek ve disk boyutunu RGB'ye kıyasla 3 kat azaltır.<br>• Hesaplama karmaşıklığını ve işlemci süresini radikal ölçüde düşürür.<br>• Kromatik gürültüyü yok eder; gradyan, doku ve kenar algılamayı basitleştirir. | • Tüm renk (krominans) bilgisini kaybeder.<br>• Eşit parlaklığa sahip farklı renkler (örneğin saf kırmızı ile saf yeşil) gri seviyede ayırt edilemez hale gelir. | • Kenar tespiti (Sobel, Canny, Prewitt, LoG)<br>• Öznitelik çıkarımı (SIFT, SURF, ORB, Harris Köşe)<br>• Karakter tanıma (OCR), morfolojik işlemler<br>• Tıbbi görüntüleme (Röntgen / X-Ray, BT, Manyetik Rezonans) |
| **CMYK** | **C:** Camgöbeği (Cyan)<br>**M:** Galibarda (Magenta)<br>**Y:** Sarı (Yellow)<br>**K:** Siyah (Key / Black) | Çıkarmalı (Subtractive)<br>Fiziksel Baskı Tabanlı | • Baskı mürekkeplerinin kağıt üzerindeki ışık soğurma fiziğiyle doğrudan örtüşür.<br>• Ayrı bir siyah mürekkep (K) kullanımı renk karışımından daha net siyah verir ve maliyeti düşürür. | • Dijital ekranlar için uygun değildir.<br>• Renk gamutu RGB'den daha dardır (ekrandaki bazı canlı renkler kağıda basılamaz). | • Matbaacılık, ofset baskı, profesyonel masaüstü yazıcılar<br>• Yayıncılık baskı öncesi (prepress) hazırlığı |

---

## 2. 1000x1000 BMP Dosya Boyutu ve Kanal Analizi

### 2.1. BMP Dosya Formatının İkili (Binary) Mimarisi

Standart Windows Bitmap (`.bmp`) dosyası sıkıştırmasız (uncompressed raw raster) bir formattır. Dosya şu katmanlardan oluşur:

1. **BITMAPFILEHEADER (14 Bayt):**
   - `bfType` (2 Bayt): İmza (`'BM'` = `0x42 0x4D`).
   - `bfSize` (4 Bayt): Toplam dosya boyutu.
   - `bfReserved1` & `bfReserved2` (4 Bayt): Ayrılmış sıfır alanları.
   - `bfOffBits` (4 Bayt): Piksel veri dizisinin başladığı bayt ofseti.
2. **BITMAPINFOHEADER (40 Bayt - DIB Header):**
   - Genişlik (1000 px), Yükseklik (1000 px), Renk Düzlemleri (1), Piksel Başına Bit Sayısı (`biBitCount`: 24 veya 8), Sıkıştırma (`0` = BI_RGB sıkıştırmasız), Görüntü Boyutu (`biSizeImage`).
3. **Renk Paleti Tablosu (Color Palette / Color Table):**
   - **24-bit Renkli BMP:** Palet yoktur (**0 Bayt**). Veri ofseti $14 + 40 = 54$ bayttır.
   - **8-bit Gri BMP:** Her biri 4 bayt olan (`RGBQUAD: Blue, Green, Red, Reserved`) 256 adet renk indeksini tutan bir palet tablosu zorunludur: $256 \times 4 = \mathbf{1024\text{ Bayt}}$. Veri ofseti $54 + 1024 = 1078$ bayttır.
4. **Satır Hizalama (4-Bayt Padding):**
   - BMP formatında her satırın bayt uzunluğu 4'ün tam katı olmak zorundadır:
     $$\text{RowStride} = \left\lfloor \frac{\text{Genişlik} \times \text{bpp} + 31}{32} \right\rfloor \times 4$$
   - 24-bit için satır uzunluğu: $1000 \times 3 = 3000$ bayt. $3000 \pmod 4 = 0$ olduğu için ek dolgu (padding) **0 bayttır**.
   - 8-bit için satır uzunluğu: $1000 \times 1 = 1000$ bayt. $1000 \pmod 4 = 0$ olduğu için ek dolgu **0 bayttır**.

---

### 2.2. Matematiksel Hesaplama ve Deneysel Sonuçlar

| Parametre / Metrik | 24-bit Renkli BMP | 8-bit Gri Seviye BMP | Açıklama / Bağıntı |
| :--- | :---: | :---: | :--- |
| **Çözünürlük** | $1000 \times 1000$ | $1000 \times 1000$ | Toplam piksel sayısı $1{,}000{,}000$ sabittir. |
| **Kanal Sayısı** | **3 Kanal** (BGR) | **1 Kanal** (Gri Luma) | Piksel başına 3 bayt vs 1 bayt |
| **Piksel Başına Bit (bpp)** | 24 bit | 8 bit | 3 bayt / 1 bayt |
| **BITMAPFILEHEADER** | 14 bayt | 14 bayt | Standart dosya başlığı |
| **BITMAPINFOHEADER** | 40 bayt | 40 bayt | Standart DIB başlığı |
| **Renk Paleti (Palette)** | **0 bayt** | **1024 bayt** | Gri seviye için $256 \times 4$ baytlık RGBQUAD |
| **Veri Başlangıç Ofseti** | 54 bayt | 1078 bayt | $54 + \text{Palet}$ |
| **Saf Piksel Matrisi Boyutu** | **3,000,000 bayt** | **1,000,000 bayt** | $1000 \times 1000 \times \text{Kanal}$ |
| **Toplam Disk Dosya Boyutu** | **3,000,054 bayt** | **1,001,078 bayt** | Başlık + Palet + Piksel Verisi |
| **Dosya Boyutu (KB / MB)** | **2,929.74 KB (2.861 MB)** | **977.62 KB (0.9547 MB)** | 1024 tabanında dönüşüm |

### 2.3. Kanal Sayısı ve Çözünürlük ile Kıyaslama Yorumu

1. **Saf Piksel Verisi Oranı:**
   $$\frac{\text{Renkli Piksel Boyutu}}{\text{Gri Piksel Boyutu}} = \frac{3{,}000{,}000\text{ bayt}}{1{,}000{,}000\text{ bayt}} = \mathbf{3.0000}$$
   Bu oran, renkli görüntünün 3 kanal (Mavi, Yeşil, Kırmızı), gri görüntünün ise tek kanal içermesinden ötürü **tam olarak kanal sayılarının oranına (3 / 1)** eşittir.
2. **Toplam Disk Dosya Boyutu Oranı:**
   $$\frac{\text{Renkli Dosya Boyutu}}{\text{Gri Dosya Boyutu}} = \frac{3{,}000{,}054\text{ bayt}}{1{,}001{,}078\text{ bayt}} \approx \mathbf{2.9968}$$
   Dosya boyutları oranı 3.0 değerine son derece yakındır ($\approx 3:1$). Tam 3.0 olmamasının yegâne nedeni, 8-bit gri seviye BMP'nin ihtiyaç duyduğu **1024 baytlık renk paleti (Color Palette Table)** ek yüküdür (overhead).
3. **Çözünürlük Etkisi:**
   Piksel sayısı genişlik $\times$ yükseklik ile karesel oranda ($O(W \cdot H)$) büyürken, sabit başlıklar (54 bayt ve 1024 bayt) toplam dosya boyutunun binde birinden bile küçüktür (%0.03). Bu nedenle yüksek çözünürlüklerde disk boyutu neredeyse tamamen $(\text{Genişlik} \times \text{Yükseklik} \times \text{Kanal Sayısı})$ çarpımıyla belirlenir.

---

## 3. Üretilen Çıktılar

- `cikti/gri_1000x1000.bmp`: 8-bit gri seviye dönüştürülmüş BMP görüntüsü ($1{,}001{,}078$ bayt).
- `cikti/boyut_analizi_raporu.txt`: İkili başlık bayt dökümü ve sayısal oranlar.
- `cikti/karsilastirma_gorsel.png`: Renkli ve gri görüntülerin, renk histogramlarının ve MB cinsinden disk boyutlarının grafiksel paneli.
- `cikti/renk_uzaylari_karsilastirma.png`: RGB, HSV, YUV ve CIE L\*a\*b\* uzaylarının 12 farklı alt kanala ayrıştırılmış detaylı görsel haritası.

---

## 4. Betiği Çalıştırma

```bash
# Otomatik mod (çıktıları üretir ve analiz eder)
python3 main.py

# Ekranda interaktif OpenCV penceresi ile görmek için:
python3 main.py --show
```
