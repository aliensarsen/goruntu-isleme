# Ödev 3.2: Histogram Eşitleme (Histogram Equalization)

Bu ödevde, CDF (Kümülatif Dağılım Fonksiyonu) tabanlı histogram eşitleme formülü sıfırdan Python ile kodlanmış ve OpenCV `cv2.equalizeHist()` fonksiyonu ile doğrulanmıştır.

## Matematiksel Formül
$$T(k) = \text{round}\left( \frac{\text{CDF}(k) - \text{CDF}_{\min}}{N - \text{CDF}_{\min}} \cdot 255 \right)$$

## Çalıştırma
```bash
python3 main.py
```

## Sonuçlar
- `sis.jpg`: Standart sapma $37.28$'den $74.33$'e yükseltilerek sisli görüntüdeki detaylar belirginleştirilmiştir.
- Kendi fonksiyonumuz ile OpenCV fonksiyonu birebir aynı sonuçları üretmiştir (Fark = 0).
