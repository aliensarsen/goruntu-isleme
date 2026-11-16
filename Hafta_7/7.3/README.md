# Ödev 7.3: Renkli BMP Görüntüsünün Renk Uzaylarına Dönüştürülmesi (HSV, HSI, YUV, CIE Lab) ve BMP Olarak Kaydedilmesi

Bu çalışma, RGB renk uzayındaki $1000 \times 1000$ boyutundaki 24-bit bir Bitmap (`.bmp`) görüntüsünü açmakta; görüntüyü **HSV, HSI, YUV ve CIE L\*a\*b\*** renk uzaylarına dönüştürmekte; her bir dönüştürülmüş görüntüyü 3-kanallı `.bmp` formatında diske kaydetmekte ve kanallarını kuramsal formüllerle incelemektedir.

---

## 1. Yöntem ve Kuramsal Dönüşüm Modelleri

### 1.1. HSV (Hue, Saturation, Value)
- **Model Türü:** Silindirik / Tekli Altıgen Koni (Hexcone).
- **Aydınlık Tanımı:** $V = \max(R, G, B)$. Üç temel renkten en yüksek şiddete sahip olanı aydınlık kabul eder.
- **Doygunluk Tanımı:**
  $$S_{HSV} = \begin{cases} 0, & V = 0 \\ \frac{V - \min(R, G, B)}{V}, & V > 0 \end{cases}$$
- **OpenCV Standartı:** $H \in [0, 180]$ (360 derece $2$'ye bölünür), $S \in [0, 255]$, $V \in [0, 255]$.
- **Kullanım Alanı:** Renk tabanlı nesne takibi, ışık değişimlerinden etkilenmeyen renk maskeleme.

---

### 1.2. HSI (Hue, Saturation, Intensity) - Gonzalez & Woods Formülasyonu
OpenCV kütüphanesinde doğrudan `COLOR_BGR2HSI` bayrağı bulunmamaktadır. Bu nedenle HSI uzayı kuramsal standart formülleriyle sıfırdan vektörize edilerek gerçeklenmiştir:
- **Model Türü:** Çift Koni / Silindir (Biconic).
- **Aydınlık/Şiddet Tanımı:**
  $$I = \frac{R + G + B}{3}$$
  (Üç kanalın aritmetik ortalamasıdır; insan algısındaki ortalama ışık enerjisini temsil eder).
- **Doygunluk Tanımı:**
  $$S_{HSI} = 1 - \frac{3}{R + G + B} \min(R, G, B) = 1 - \frac{\min(R, G, B)}{I} \quad (I > 0)$$
- **Ton (Hue) Açısı:**
  $$\theta = \arccos\left( \frac{\frac{1}{2}[(R - G) + (R - B)]}{\sqrt{(R - G)^2 + (R - B)(G - B)} + \epsilon} \right)$$
  $$H = \begin{cases} \theta, & B \le G \\ 360^\circ - \theta, & B > G \end{cases}$$
- **8-Bit BMP Ölçeklemesi:** $H_{8u} = \text{round}\left(\frac{H}{360} \times 255\right)$, $S_{8u} = \text{round}(S \times 255)$, $I_{8u} = \text{round}(I \times 255)$.

> [!IMPORTANT]
> **HSV ile HSI Arasındaki Kritik Fark:**
> - **HSV:** $V = \max(R, G, B)$ değerini kullanır; bu nedenle örneğin saf kırmızı $(255, 0, 0)$ ile saf beyaz $(255, 255, 255)$ aynı parlaklığa ($V = 255$) sahiptir.
> - **HSI:** $I = (R + G + B) / 3$ değerini kullanır; saf kırmızının şiddeti $I = 85$, saf beyazın şiddeti ise $I = 255$'tir. HSI, fotometrik ışık enerjisini daha gerçekçi modeller.

---

### 1.3. YUV (Luma Y, U-Chroma, V-Chroma)
- **Model Türü:** Aydınlık ve Krominans Ayrışımı (ITU-R BT.601).
- **Formüller:**
  $$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$
  $$U = 0.492 \cdot (B - Y) + 128 = -0.147 \cdot R - 0.289 \cdot G + 0.436 \cdot B + 128$$
  $$V = 0.877 \cdot (R - Y) + 128 = 0.615 \cdot R - 0.515 \cdot G - 0.100 \cdot B + 128$$
- **Özellik:** $Y$ kanalı insan gözünün en duyarlı olduğu gri aydınlığı taşır. $U$ ve $V$ renk farklarıdır ($+128$ ofsetiyle 8-bit pozitif tamsayı aralığına ötelenir).
- **Kullanım Alanı:** Video sıkıştırma kodekleri (H.264, HEVC, VP9, AV1) ve televizyon yayıncılığı.

---

### 1.4. CIE L\*a\*b\* (CIELAB)
- **Model Türü:** Algısal Olarak Düzgün (Perceptually Uniform), Cihazdan Bağımsız.
- **Bileşenler:**
  - $L^*$: Algısal aydınlık ($0$ siyah, $100$ beyaz $\rightarrow$ 8-bitte $0 - 255$ aralığına ölçeklenir).
  - $a^*$: Yeşil $\leftrightarrow$ Kırmızı renk ekseni (negatif değerler yeşil, pozitif değerler kırmızı).
  - $b^*$: Mavi $\leftrightarrow$ Sarı renk ekseni (negatif değerler mavi, pozitif değerler sarı).
- **Özellik:** Renkler arası Öklid mesafesi ($\Delta E$) insan gözünün renkleri ayırt etme eşiğine (JND) tam orantılıdır.

---

## 2. Üretilen BMP Dosyaları ve Boyut Analizi

Tüm çıktılar sıkıştırmasız 24-bit TrueColor BMP olarak kaydedilmiştir:

| Renk Uzayı | Çıktı Dosyası | Çözünürlük | Kanal Sayısı | Bit Derinliği | Disk Boyutu |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Girdi (BGR)** | `girdi/renkli_1000x1000.bmp` | $1000 \times 1000$ | 3 | 24-bit | $3{,}000{,}054\text{ bayt}$ (~$2.86\text{ MB}$) |
| **HSV** | `cikti/resim_hsv.bmp` | $1000 \times 1000$ | 3 | 24-bit | $3{,}000{,}054\text{ bayt}$ (~$2.86\text{ MB}$) |
| **HSI** | `cikti/resim_hsi.bmp` | $1000 \times 1000$ | 3 | 24-bit | $3{,}000{,}054\text{ bayt}$ (~$2.86\text{ MB}$) |
| **YUV** | `cikti/resim_yuv.bmp` | $1000 \times 1000$ | 3 | 24-bit | $3{,}000{,}054\text{ bayt}$ (~$2.86\text{ MB}$) |
| **CIE Lab** | `cikti/resim_cielab.bmp` | $1000 \times 1000$ | 3 | 24-bit | $3{,}000{,}054\text{ bayt}$ (~$2.86\text{ MB}$) |

> [!NOTE]
> Her bir dönüştürülmüş görüntü 3 adet 8-bit kanaldan oluştuğu için piksel dizisi $1000 \times 1000 \times 3 = 3{,}000{,}000\text{ bayt}$ tutar. 54 baytlık BMP başlığı ile birlikte tüm BMP dosyalarının disk boyutu tam olarak **$3{,}000{,}054\text{ bayt}$**tır.

---

## 3. Üretilen Çıktılar

- `cikti/resim_hsv.bmp`: 3-kanallı HSV BMP görüntüsü.
- `cikti/resim_hsi.bmp`: 3-kanallı HSI BMP görüntüsü.
- `cikti/resim_yuv.bmp`: 3-kanallı YUV BMP görüntüsü.
- `cikti/resim_cielab.bmp`: 3-kanallı CIE L\*a\*b\* BMP görüntüsü.
- `cikti/renk_uzaylari_paneli.png`: $5 \times 4$ ızgarada tüm uzayların ve alt kanallarının (R, G, B, H, S, V, I, Y, U, V, L\*, a\*, b\*) detaylı karşılaştırma paneli.
- `cikti/donusum_raporu.txt`: Kanal istatistikleri (Min, Max, Ortalama, Std. Sapma) ve kuramsal karşılaştırma metni.

---

## 4. Çalıştırma

```bash
python3 main.py
```
*(Betik, `../girdi/renkli_1000x1000.bmp` görselini otomatik olarak okur, tüm uzaylara dönüştürür, BMP'leri ve analiz görselini üretir).*
