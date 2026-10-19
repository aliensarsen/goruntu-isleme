# Ödev 5.1: Renkli Görüntü Kanal Histogramları ve Siyah-Beyaz Dönüşümü

Bu ödevde:
1. Renkli bir görüntü okunarak **Mavi (B)**, **Yeşil (G)** ve **Kırmızı (R)** kanallarının her biri için histogram çıkarılmıştır.
2. Görüntü hem **Gri Tonlamaya (Grayscale)** hem de **İkili Siyah-Beyaz'a (Sabit Eşikleme ve Otsu Algoritması)** dönüştürülmüştür.
3. Çıktılar ve karşılaştırmalı analiz paneli kaydedilmiştir.

## Çalıştırma
```bash
python3 main.py
```
*(Kendi resminizle çalıştırmak için: `python3 main.py resminiz.jpg`)*

## Çıktı Dosyaları
- `output_grayscale.jpg`: 8-bit gri seviye görsel.
- `output_binary_fixed.jpg`: Sabit eşikleme (127) ile ikili siyah-beyaz görsel.
- `output_binary_otsu.jpg`: Otsu algoritması ile otomatik eşiklenmiş siyah-beyaz görsel.
- `histogram_analiz_sonucu.png`: 6 panelli karşılaştırma grafiği.
