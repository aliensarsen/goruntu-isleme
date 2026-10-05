# Ödev 3.1: Min-Max Doğrusal Kontrast Germe

Bu ödevde, dinamik aralığı dar olan `dag.jpg` ve `sis.jpg` görüntüleri, piksel değerleri $[0, 255]$ aralığına tam yayılacak şekilde doğrusal olarak ölçeklenmiştir.

## Matematiksel İfade
$$y = \frac{x - x_{\min}}{x_{\max} - x_{\min}} \cdot 255$$

## Çalıştırma
```bash
python3 main.py
```

## Sonuçlar
- `dag`: 0-237 aralığından 0-255 aralığına gerildi.
- `sis`: 92-249 aralığından 0-255 aralığına gerildi.
- Özel formül ve `cv2.normalize(..., cv2.NORM_MINMAX)` çıktıları birebir özdeştir (Maksimum Fark = 0).
