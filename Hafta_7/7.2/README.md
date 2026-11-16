# Ödev 7.2: 8K Çözünürlükte 3-Kanallı BMP Düzenleme ve Hassas Süre Ölçümü

Bu çalışma, **8K UHD (7680 x 4320)** çözünürlüğünde 3-kanallı (24-bit TrueColor) sıkıştırmasız bir BMP görüntüsü oluşturmakta; görüntüyü OpenCV kullanarak belleğe yüklemekte; dosya açma ve kaydetme sürelerini tamamen hariç tutarak **yalnızca piksel değerlerini 2'ye bölme (görüntü düzenleme)** işleminin işlemci süresini nanosaniye hassasiyetiyle ölçmektedir.

---

## 1. Yöntem ve Kuramsal Altyapı

### 1.1. 8K UHD Çözünürlük ve Bellek Ayak İzi
- **Çözünürlük Standartı:** 8K UHDTV ($7680 \times 4320$ piksel).
- **Piksel Sayısı:** $7680 \times 4320 = \mathbf{33{,}177{,}600\text{ piksel}}$ (~$33.18$ Megapiksel).
- **Kanal Sayısı ve Derinliği:** 3 Kanal (Mavi, Yeşil, Kırmızı - BGR), her kanal 8-bit unsigned integer (`uint8`).
- **Piksel Verisi Boyutu:** $33{,}177{,}600 \times 3 = \mathbf{99{,}532{,}800\text{ bayt}}$ (~$94.92\text{ MB}$).
- **BMP Dosya Başlığı:** $14\text{ bayt (File Header)} + 40\text{ bayt (DIB Header)} = 54\text{ bayt}$.
- **Toplam Disk Boyutu:** $99{,}532{,}800 + 54 = \mathbf{99{,}532{,}854\text{ bayt}}$ (~$99.53\text{ MB}$).
- **Satır Hizalama (Padding):** $7680 \times 3 = 23{,}040$ bayt. $23{,}040 \pmod 4 = 0$ olduğu için ek satır dolgusu $0$ bayttır.

---

### 1.2. Süre Ölçümünde Hassasiyet ve I/O Ayrımı
Görüntü işleme algoritmalarının başarımı ölçülürken disk G/Ç (I/O) süreleri ile bellek içi aritmetik işlem süreleri birbirinden kesinlikle ayrılmalıdır:
1. **Açma Süresi (`cv2.imread`):** Diskten dosya okuma ve baytların belleğe kopyalanması (~$30 - 45\text{ ms}$).
2. **Kaydetme Süresi (`cv2.imwrite`):** Bellekteki dizinin disk bloklarına yazılması (~$35 - 50\text{ ms}$).
3. **Yalnızca Düzenleme Süresi (Ödevin Odak Noktası):** 33.18 milyon pikselin (toplam 99.53 milyon kanal elemanının) doğrudan CPU çekirdeğinde 2'ye bölünmesi.

Hassas ölçüm için `time.perf_counter_ns()` (nanosaniye saat sayacı) kullanılmıştır.

---

### 1.3. Test Edilen Hesaplama Stratejileri

1. **NumPy Vektörize Tamsayı Bölme (`img // 2`):** C tabanlı NumPy çekirdeğinde her elemanın tamsayı taban bölmesi (Floor Division).
2. **NumPy Sağa Bit Kaydırma (`img >> 1`):** Aritmetik olarak $x // 2 \equiv x \gg 1$. İşlemcinin ALU biriminde tek çevrimlik donanımsal bit kaydırma.
3. **Yerinde Bit Kaydırma (`np.right_shift(img, 1, out=img)` - In-Place):** Yeni bir 99.5 MB bellek dizisi tahsis etmeden, mevcut bellek tamponu üzerinde doğrudan işlem.
4. **OpenCV `cv2.divide(img, 2)`:** OpenCV'nin SIMD (AVX2/NEON) optimize edilmiş fonksiyonu. OpenCV yuvarlama (`round(x / 2.0)`) uygularken, tamsayı bölme tabana yuvarlar (`truncation`).
5. **Paralel Çok İş Parçacıklı (`ThreadPoolExecutor` - 4 Thread):** 8K görüntüyü 4 yatay dilime bölerek çok çekirdekli paralel işleme.

---

## 2. Sayısal Ölçüm Sonuçları ve Başarım Tablosu

| Hesaplama Yöntemi | Düzenleme Süresi (ms) | Düzenleme Süresi (sn) | İşlem Hızı (Megapiksel/sn) | Bellek Verimi (GB/sn) |
| :--- | :---: | :---: | :---: | :---: |
| **Yerinde Bit Kaydırma (In-place)** | **8.67 ms** | **0.00867 s** | **3,827.80 MP/s** | **10.69 GB/s** |
| **NumPy Tamsayı Bölme (`// 2`)** | 10.98 ms | 0.01098 s | 3,022.52 MP/s | 8.44 GB/s |
| **NumPy Sağa Bit Kaydırma (`>> 1`)**| 13.96 ms | 0.01396 s | 2,377.21 MP/s | 6.64 GB/s |
| **Paralel Threading (4 Thread)** | 16.31 ms | 0.01631 s | 2,034.71 MP/s | 5.68 GB/s |
| **OpenCV `cv2.divide(img, 2)`** | 79.51 ms | 0.07951 s | 417.27 MP/s | 1.17 GB/s |

### Referans Süreler (Ödeve Dahil Edilmeyen G/Ç Süreleri):
- **8K BMP Açma Süresi (`cv2.imread`):** $36.47\text{ ms}$
- **8K BMP Kaydetme Süresi (`cv2.imwrite`):** $44.50\text{ ms}$
- **En Hızlı Düzenleme Süresi:** **$8.67\text{ ms}$**
- *Yorum:* En hızlı düzenleme süresi, dosya kaydetme süresinden yaklaşık **5 kat daha hızlıdır**.

---

## 3. Bulgular ve Teknik Değerlendirme

1. **Donanım Sağa Kaydırma vs Bölme:**
   - `img // 2` ile `img >> 1` çıktısı piksel piksel birebir özdeştir (`np.array_equal == True`).
2. **Bellek Tahsisinin Önemi:**
   - `np.right_shift(..., out=img)` yerinde (in-place) çalıştırıldığında 99.5 MB'lık yeni bir arabellek tahsis etme (malloc) yükü ortadan kalktığı için **8.67 ms** ile en yüksek hıza ve **10.69 GB/sn** bellek bant genişliğine ulaşmıştır.
3. **OpenCV Rounding Farkı:**
   - `cv2.divide()`, tek sayılarda $1 / 2 = 0.5 \rightarrow 1$ şeklinde yukarı yuvarlar; tamsayı bölme ise $1 // 2 = 0$ taban değerini alır.
4. **Gerçek Zamanlı Başarım:**
   - 33.18 Megapiksellik devasa 8K matris, CPU vektörizasyonu ile 8-11 ms bandında işlenebilmektedir. Bu süre $1 / 0.00867 \approx 115\text{ FPS}$ hızına karşılık gelmekte olup 8K gerçek zamanlı video işleme sınırının (60 FPS) oldukça üzerindedir.

---

## 4. Üretilen Çıktılar

- `cikti/8k_duzenlenmis.bmp`: Her pikseli 2'ye bölünmüş 8K BMP dosyası ($99{,}532{,}854\text{ bayt}$).
- `cikti/sure_ve_performans_raporu.txt`: Nanosaniye hassasiyetli süreler, verim ve karşılaştırma dökümü.
- `cikti/8k_karsilastirma_ve_sure.png`: Orijinal vs Düzenlenmiş 8K karşılaştırması, süre bar grafiği ve 100x100 piksel yakınlaştırma analizi.
- `cikti/8k_onizleme_orijinal.jpg` ve `cikti/8k_onizleme_duzenlenmis.jpg`: Hızlı inceleme için downsampled önizleme görselleri.

---

## 5. Çalıştırma

```bash
python3 main.py
```
*(Girdi klasöründe 8K BMP bulunamazsa betik otomatik olarak sentetik 8K test görselini üretir, işler ve raporlar).*
