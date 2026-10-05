# Ödev 3.3: CLAHE (Contrast Limited Adaptive Histogram Equalization)

Bu ödevde, global histogram eşitlemenin gürültüyü aşırı yükseltme sorununu çözen CLAHE algoritması uygulanmıştır.

## Parametreler
- **Kırpma Eşiği (Clip Limit):** 2.0
- **Karo Izgarası (Tile Grid Size):** 8x8 (64 yerel bölge)

## Çalıştırma
```bash
python3 main.py
```

## Sonuçlar
- Yerel kontrast sınırlandırılarak sisli görüntüdeki detaylar doğal bir ton aralığında açılmıştır.
- Kendi yazdığımız bilinear enterpolasyonlu CLAHE algoritması ile OpenCV çıktısı karşılaştırılmış; yalnızca karo sınırlarında float yuvarlamasından kaynaklı %0.2'den az pikselde maksimum 1 birimlik fark oluştuğu gözlemlenmiştir.
