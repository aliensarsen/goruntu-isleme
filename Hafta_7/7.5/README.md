# Ödev 7.5 (Görev 5): RGB, YCbCr ve HSV ile Ten Rengi Tespiti ve Ten Dışı Alanları Tam Kırmızı Gösterme

Bu çalışma, farklı etnik kökenlerden 21 farklı insan yüzünün ve canlı renkli arka plan bloklarının yer aldığı bir görüntü üzerinde; **RGB, YCbCr ve HSV** renk uzaylarında ten rengi segmentasyonu gerçekleştirmekte; ten olmayan tüm bölgeleri **tam kırmızı (BGR: `[0, 0, 255]`)** renge boyamakta ve ten tespiti problemi için renk uzaylarının başarım farklarını karşılaştırmaktadır.

---

## 1. Yöntem ve Kuramsal Altyapı

İnsan ten rengi biyolojik olarak derideki **melanin** ve **hemoglobin** pigmentlerinin ışığı soğurma ve yansıtma özellikleriyle belirlenir. Etnik kökene bağlı olarak tenin açık veya koyu olması büyük oranda aydınlık şiddetini ($Y$ veya $V$) değiştirirken, renk tonu (kroma/hue) şaşırtıcı şekilde dar ve tutarlı bir alanda toplanır.

### 1.1. RGB Renk Uzayında Ten Tespiti
RGB uzayında renk (krominans) ile aydınlık (luminans) birbirinden ayrılamadığı için karmaşık eşik kuralları kullanılır (Peer et al., 2003):
- $R > 95$ ve $G > 40$ ve $B > 20$
- $\max(R, G, B) - \min(R, G, B) > 15$
- $|R - G| > 15$
- $R > G$ ve $R > B$

**RGB'nin Temel Zafiyeti:**
Görüntüdeki parlak **sarı, turuncu ve kırmızı arka plan kutuları** da $R > G > B$ şartını sağladığı için RGB kuralında yanlışlıkla ten olarak algılanır (Yüksek Yanlış Pozitif / False Positive). Ayrıca koyu tenli bireylerin gölgede kalan yüz kısımları $R > 95$ eşiğine takılarak elenir (Yanlış Negatif / False Negative).

---

### 1.2. YCbCr Renk Uzayında Ten Tespiti (Daha Uygun Renk Uzayı)
- **Dönüşüm:** `cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)`
- **Kural (Chai & Ngan, Kovac et al.):**
  $$133 \le Cr \le 173$$
  $$77 \le Cb \le 127$$
- **Neden Daha Uygun?**
  Aydınlık bilgisi ($Y$) tamamen devre dışı bırakılır. Kroma düzleminde ($Cb, Cr$) Kafkas, Asyalı, Afrikalı ve Latin tenleri aynı eliptik kümede toplanır. Ten koyulaşsa bile kroma değerleri neredeyse sabittir, yalnızca $Y$ azalır. Bu sayede görseldeki tüm yüzler arka planlardan başarıyla ayrıştırılır.

---

### 1.3. HSV Renk Uzayında Ten Tespiti (Daha Uygun Renk Uzayı)
- **Dönüşüm:** `cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)`
- **Kural:**
  $$\text{Ton (Hue)}: (0 \le H \le 22) \lor (170 \le H \le 180)$$
  $$\text{Doygunluk (Saturation)}: 35 \le S \le 190$$
  $$\text{Parlaklık (Value)}: V \ge 50$$
- **Neden Daha Uygun?**
  Ton ($H$) kanalı ortam ışığından bağımsız saf renk dalga boyunu temsil eder. İnsan teni kırmızı-turuncu-sarı bandında ($0^\circ - 45^\circ$) yer alır. Doygunluk ($S$) eşiği eklenerek aşırı parlak yapay sarı/turuncu arka planlar kolaylıkla elenir.

---

### 1.4. Ten Olmayan Bölgelerin Tam Kırmızı Yapılması
Hocanın yönergesi doğrultusunda:
$$\text{Piksel Çıktısı} = \begin{cases} \text{Orijinal BGR}, & \text{Eğer Piksel Ten İse} (\text{Maske} = 1) \\ [0, 0, 255] \text{ (Tam Kırmızı)}, & \text{Eğer Piksel Ten Değil İse} (\text{Maske} = 0) \end{cases}$$

---

## 2. Sayısal Sonuçlar ve Karşılaştırma Tablosu

| Renk Uzayı | Model Türü | Tespit Edilen Ten Pikseli | Oran (%) | Arka Plan Ayırt Etme Başarımı |
| :--- | :--- | :---: | :---: | :--- |
| **RGB** | Kartezyen Küp (Peer et al.) | $144{,}144$ | %27.71 | **Zayıf:** Sarı ve turuncu arka planları ten sanarak maskeler. |
| **YCbCr** | Ayrık Luma + Kroma ($Cr, Cb$) | $\mathbf{146{,}793}$ | **%28.22** | **Mükemmel:** Farklı ten renklerini kroma düzleminde eksiksiz yakalar. |
| **HSV** | Silindirik ($H, S, V$) | $133{,}217$ | %25.61 | **Çok Yüksek:** Doygunluk eşiğiyle yapay arka planları tamamen eler. |

---

## 3. Üretilen Çıktılar

- `cikti/ten_rgb.png`: RGB ile ten tespiti yapılmış, ten dışı tam kırmızı görüntü.
- `cikti/ten_ycbcr.png`: YCbCr ile ten tespiti yapılmış, ten dışı tam kırmızı görüntü.
- `cikti/ten_hsv.png`: HSV ile ten tespiti yapılmış, ten dışı tam kırmızı görüntü.
- `cikti/karsilastirma_ten_paneli.png`: Orijinal, RGB, YCbCr ve HSV sonuçlarının yan yana $2 \times 2$ karşılaştırma paneli.
- `cikti/ten_maskeleri_paneli.png`: Üç renk uzayının ikili (binary) siyah-beyaz ten maskeleri.
- `cikti/ten_tespiti_raporu.txt`: Sayısal piksel dökümü ve teknik tartışma metni.

---

## 4. Çalıştırma

```bash
python3 main.py
```
*(Betik `../girdi/insan_tenleri.jpg` görselini açar, üç uzayda da ten tespiti yapar, ten dışı bölgeleri kırmızıya boyar ve panelleri kaydeder).*
