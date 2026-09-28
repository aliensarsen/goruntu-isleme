# Ödev 2.3: Parça Histogramlarını Thread ile Hesaplayıp Birleştirme

Bu ödevde, görüntünün 4 eşit parçasının histogramı `ThreadPoolExecutor` kullanılarak paralel olarak hesaplanmış, ardından toplanarak ana görüntü histogramı ile karşılaştırılmıştır.

## Doğrulama
- 4 parçadan gelen histogramların toplamı ile tüm görüntünün tek seferde hesaplanan histogramı karşılaştırılmış ve **aralarında 0 fark olduğu (birebir özdeşlik)** doğrulanmıştır.

## Çalıştırma
```bash
python3 main.py
```

## Üretilen Çıktılar
- `cikti/histogram.png`: Birleştirilmiş gri seviye histogram grafiği.
- `cikti/histogram_thread_cikti.txt`: Doğrulama raporu.
