# Ödev 7.2 (Görev 2): 1000x1000 BMP Dosya Boyutu ve Kanal Analizi

Bu çalışma, $1000 \times 1000$ boyutundaki 24-bit renkli ve 8-bit gri seviye BMP (Bitmap) formatındaki görüntülerin disk ayak izlerini çözünürlük, kanal sayısı ve ikili (binary) dosya başlık yapısı düzeyinde incelemektedir.

---

## 1. Yöntem ve BMP Mimarisi

Standart Windows Bitmap (`.bmp`) formatı sıkıştırmasız (uncompressed raw raster) bir formattır:
1. **BITMAPFILEHEADER (14 Bayt):** Dosya türü (`'BM'`), toplam dosya boyutu, piksel veri başlangıç ofseti.
2. **BITMAPINFOHEADER (40 Bayt - DIB Header):** Genişlik (1000), yükseklik (1000), bit derinliği (24 veya 8).
3. **Renk Paleti (Color Table):**
   - **24-bit Renkli BMP:** Palet yoktur (**0 Bayt**). Veri ofseti $14 + 40 = 54$ bayttır.
   - **8-bit Gri BMP:** 256 renk indeksini tutan `RGBQUAD[256]` palet tablosu zorunludur: $256 \times 4 = \mathbf{1024\text{ Bayt}}$. Veri ofseti $54 + 1024 = 1078$ bayttır.
4. **Satır Hizalama (Padding):**
   - Her satırın bayt uzunluğu 4'ün tam katı olmalıdır.
   - 24-bit için satır uzunluğu: $1000 \times 3 = 3000$ bayt ($3000 \pmod 4 = 0$, dolgu 0 bayt).
   - 8-bit için satır uzunluğu: $1000 \times 1 = 1000$ bayt ($1000 \pmod 4 = 0$, dolgu 0 bayt).

---

## 2. Karşılaştırma ve Matematiksel İspat

| Parametre / Metrik | 24-bit Renkli BMP | 8-bit Gri Seviye BMP | Açıklama / Bağıntı |
| :--- | :---: | :---: | :--- |
| **Çözünürlük** | $1000 \times 1000$ | $1000 \times 1000$ | Piksel sayısı $1{,}000{,}000$ sabittir |
| **Kanal Sayısı** | **3 Kanal** (BGR) | **1 Kanal** (Gri Luma) | Piksel başına 3 bayt vs 1 bayt |
| **Piksel Başına Bit (bpp)** | 24 bit | 8 bit | 3 bayt / 1 bayt |
| **BMP Başlıkları (File+DIB)** | 54 bayt | 54 bayt | Standart DIB başlığı |
| **Renk Paleti Tablosu** | **0 bayt** | **1024 bayt** | Gri seviye için $256 \times 4$ baytlık RGBQUAD |
| **Piksel Veri Başlangıç Ofseti**| 54 bayt | 1078 bayt | $54 + \text{Palet}$ |
| **Saf Piksel Matrisi Boyutu** | **3,000,000 bayt** | **1,000,000 bayt** | $1000 \times 1000 \times \text{Kanal}$ |
| **Toplam Disk Dosya Boyutu** | **3,000,054 bayt** | **1,001,078 bayt** | Başlık + Palet + Piksel Verisi |
| **Disk Boyutu (KB / MB)** | **2,929.74 KB (~2.86 MB)** | **977.62 KB (~0.95 MB)** | 1024 tabanında dönüşüm |

### Değerlendirme:
1. **Saf Piksel Verisi Oranı:**
   $$\frac{3{,}000{,}000\text{ bayt}}{1{,}000{,}000\text{ bayt}} = \mathbf{3.0000}$$
   Bu oran doğrudan kanal sayılarının oranına ($3 / 1$) eşittir.
2. **Toplam Dosya Boyutu Oranı:**
   $$\frac{3{,}000{,}054\text{ bayt}}{1{,}001{,}078\text{ bayt}} \approx \mathbf{2.9968}$$
   Tam 3.0 olmamasının yegâne nedeni, 8-bit gri BMP'deki **1024 baytlık renk paleti** ek yüküdür.

---

## 3. Üretilen Çıktılar

- `cikti/gri_1000x1000.bmp`: 8-bit gri seviye BMP görüntüsü ($1{,}001{,}078\text{ bayt}$).
- `cikti/boyut_analizi_raporu.txt`: İkili başlık dökümü ve sayısal oranlar.
- `cikti/karsilastirma_gorsel.png`: Renkli ve gri görüntülerin, renk histogramlarının ve disk boyutlarının grafiksel paneli.

---

## 4. Çalıştırma

```bash
python3 main.py

# Ekranda interaktif OpenCV penceresi açmak için:
python3 main.py --show
```
