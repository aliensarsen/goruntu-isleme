# Ödev 5.2: Özel calcHist Fonksiyonu ve Kanal Histogramları

Bu ödevde:
1. `cv2.calcHist()` kullanılmadan, saf Python/NumPy ile 0–255 parlaklık frekanslarını hesaplayan `custom_calc_hist` fonksiyonu yazılmıştır.
2. Bu fonksiyon renkli görüntünün her bir renk kanalı (Mavi, Yeşil, Kırmızı) için ayrı ayrı çalıştırılmıştır.
3. Çıktılar OpenCV'nin hazır fonksiyonu ile kıyaslanmış ve **farkın 0.0 (birebir özdeş)** olduğu doğrulanmıştır.

## Algoritma
```python
def custom_calc_hist(channel_matrix):
    hist = np.zeros(256, dtype=np.int64)
    for pixel in channel_matrix.ravel():
        hist[pixel] += 1
    return hist
```

## Çalıştırma
```bash
python3 main.py
```
*(Kendi resminizle: `python3 main.py resminiz.jpg`)*

## Çıktı Dosyaları
- `custom_histogram_grafikleri.png`: Kanalların ayrı ayrı ve birleşik histogram grafiği.
