# Ödev 6.3: OpenCV HoughCircles ile Çember Tespiti

Bu ödevde, Smarties renkli şeker görüntüsü üzerinde Canny kenarları ve $3 \times 3$ medyan filtresi sonrasında OpenCV'nin `cv2.HoughCircles` fonksiyonu (`cv2.HOUGH_GRADIENT`) ile dairesel nesneler tespit edilmiştir.

---

## 1. Yöntem ve Parametreler

- **Kenar Algılama:** $50 - 150$ Canny ve $3 \times 3$ medyan parazit temizleme.
- **HOUGH_GRADIENT:** 3B akümülatör yerine kenar normali (gradyan yönü) boyunca 2B merkez oylaması ve ardından 1B yarıçap oylaması yaparak hesaplama yükünü azaltır.
- **Parametreler:**
  - `dp = 2`: Akümülatör çözünürlüğünün giriş görüntüsünün yarısı olması (oy yoğunluğunu artırır).
  - `minDist = 30`: İki çember merkezi arasındaki asgari mesafe.
  - `minRadius = 20`, `maxRadius = 40`: Şeker boyutlarına uygun yarıçap aralığı.
  - `param2 = 20`: Akümülatör eşik oyu.

---

## 2. Çıktılar

- `cikti/kenar_canny.png`: Canny kenar haritası.
- `cikti/kenar_median.png`: $3 \times 3$ medyan filtreli kenarlar.
- `cikti/cemberler_houghcircles.png`: Tespit edilen çemberlerin (camgöbeği) ve merkezlerin (kırmızı) çizildiği sonuç.
- `cikti/rapor.txt`: Bulunan çemberlerin merkez koordinatları ve yarıçapları.

---

## 3. Çalıştırma

```bash
python3 main.py
```
