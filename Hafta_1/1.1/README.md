# Ödev 1.1: Klasördeki Resimleri 1024x768 Boyutuna Ölçekleme

Bu ödevde, bir klasör içindeki farklı çözünürlük ve en-boy oranlarındaki görseller taranarak otomatik olarak **1024x768** piksel boyutuna yeniden ölçeklenmektedir.

## Yöntem ve Açıklama
- **Enterpolasyon Yöntemi:** Görüntü küçültülürken piksel kayıplarını ve örtüşme (*aliasing*) bozulmalarını engellemek için alan tabanlı `cv2.INTER_AREA` enterpolasyonu tercih edilmiştir.
- **Hata Yönetimi:** Klasördeki bozuk ya da okunamayan dosyalarda programın çökmesi engellenmiş, geçersiz dosyalar atlanarak raporlanmıştır.

## Çalıştırma
```bash
python3 main.py
# veya özel girdi/çıktı klasörleri ile:
python3 main.py /girdi/yolu /cikti/yolu
```

## Sonuçlar
- `girdi/dama.jpg` (1600x1066) -> `cikti/dama.jpg` (1024x768)
- `girdi/dikey.jpg` (1066x1600) -> `cikti/dikey.jpg` (1024x768)
- `girdi/kucuk.png` (400x300) -> `cikti/kucuk.png` (1024x768)
- Ölçüm detayları `cikti/resize_cikti.txt` dosyasına kaydedilmiştir.
