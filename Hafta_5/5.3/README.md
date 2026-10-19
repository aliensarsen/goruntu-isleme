# Ödev 5.3: Özel Gri Dönüşüm ve OpenCV Mutlak Hata Analizi

Bu ödevde:
1. Renkli görüntü OpenCV hazır fonksiyonu (`cv2.cvtColor`) ile gri tonlamaya çevrilmiştir.
2. Aynı görüntü ITU-R BT.601 standardına göre kendi yazdığımız `custom_bgr2gray` fonksiyonu ile gri tonlamaya çevrilmiştir:
   $$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$
3. İki görseldeki eşleşen piksellerin mutlak farklarının toplamı (SAD) hata değeri olarak hesaplanmış ve raporlanmıştır.

## Hata Sonuçları
- **Toplam Mutlak Hata (SAD):** `7` (120.000 pikselde)
- **Ortalama Mutlak Hata (MAE):** `0.000058` piksel
- **Maksimum Piksel Farkı:** `1`
- **Birebir Eşleşme Oranı:** `%99.99`

## Çalıştırma
```bash
python3 main.py
```
*(Kendi resminizle: `python3 main.py resminiz.jpg`)*

## Çıktı Dosyaları
- `output_gray_opencv.jpg`: OpenCV çıktısı.
- `output_gray_custom.jpg`: Özel fonksiyon çıktısı.
- `gri_donusum_ve_hata_analizi.png`: 4 panelli karşılaştırma ve hata haritası.
