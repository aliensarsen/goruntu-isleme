# Ödev 6.1: OpenCV HoughLines ve HoughLinesP ile Doğru Tespiti

Bu ödevde, Sudoku ızgara görüntüsü üzerinde kenar tespiti sonrasında OpenCV'nin standart ve olasılıksal Hough doğru dönüşüm algoritmaları karşılaştırılmıştır.

---

## 1. Yöntem ve Ön İşleme

1. **Kenar Tespiti:** Gri seviye Sudoku görüntüsüne $50 - 150$ eşik değerleriyle Canny uygulanmıştır.
2. **Medyan Filtresi:** Kenarlar üzerindeki 1-2 piksellik izole parazitleri temizlemek ve oylama kirliliğini önlemek amacıyla $3 \times 3$ medyan filtresi uygulanmıştır.
3. **Standart Hough Doğru Dönüşümü (`cv2.HoughLines`):**
   - Polar doğru formülü: $\rho = x \cos\theta + y \sin\theta$.
   - Sonsuz uzanan doğruları $(\rho, \theta)$ parametreleriyle tespit eder (Kırmızı çizgiler).
4. **Olasılıksal Hough Doğru Dönüşümü (`cv2.HoughLinesP`):**
   - Rastgele piksel alt kümelerini oylayarak uç noktaları $(x_1, y_1) \rightarrow (x_2, y_2)$ olan sonlu doğru parçalarını bulur (Yeşil çizgiler).

---

## 2. Çıktılar

- `cikti/kenar_canny.png`: Ham Canny kenarları.
- `cikti/kenar_median.png`: $3 \times 3$ medyan filtresi uygulanmış kenar haritası.
- `cikti/dogrular_houghlines.png`: Standart Hough ile tespit edilen doğrular (Kırmızı).
- `cikti/dogrular_houghlinesp.png`: Olasılıksal Hough ile tespit edilen doğru segmentleri (Yeşil).
- `cikti/rapor.txt`: Sayısal doğru ve kenar piksel sayıları.

---

## 3. Çalıştırma

```bash
python3 main.py
```
