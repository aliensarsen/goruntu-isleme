# Ödev 6.2: Özel Hough Doğru Dönüşümü ve Oylama Matrisi Analizi

Bu ödevde, OpenCV'nin hazır Hough fonksiyonları kullanılmadan, polar doğru modeli ($\rho, \theta$) sıfırdan Python ve NumPy ile gerçeklenmiştir.

---

## 1. Yöntem ve Algoritmik Adımlar

1. **Ön Hesaplama (LUT):** $\theta \in [0, 180^\circ)$ aralığında $1^\circ$ adımlarla $\cos\theta$ ve $\sin\theta$ tablosu belleğe alınır.
2. **Oylama (Accumulator):**
   - Her kenar noktası $(x, y)$ için 180 farklı açı taranarak $\rho = x \cos\theta + y \sin\theta$ hesaplanır.
   - $[\rho + \text{köşegen}, \theta]$ hücresine 1 oy eklenir.
3. **Yerel Tepe Tespiti (Non-Maximum Suppression):**
   - Komşu piksellerin aynı doğruya oy vermesiyle oluşan kalınlaşmayı önlemek için $3 \times 3$ morfolojik genişletme (`cv2.dilate`) ile yerel maksimumlar filtrelenir.
   - Belirlenen eşik (100 oy) üzerindeki tepeler doğrulanmış çizgi olarak kabul edilir.

---

## 2. Çıktılar

- `cikti/oylama_matrisi.png`: $\rho - \theta$ parametre uzayının renklendirilmiş (Inferno) oylama haritası.
- `cikti/dogrular_kendi.png`: Özgün algoritma ile bulunan doğruların mor renkle çizildiği Sudoku görüntüsü.
- `cikti/rapor.txt`: Tespit edilen doğruların $\rho$, $\theta$ değerleri ve oy sayıları.

---

## 3. Çalıştırma

```bash
python3 main.py
```
