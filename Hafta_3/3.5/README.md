# Ödev 3.5: 5x5 Medyan Filtresi ile Tuz-Biber Gürültüsü Temizleme ve PSNR Analizi

Bu ödevde, tuz-biber (salt & pepper / impulsif) gürültüsü içeren görüntülere 5x5 medyan filtresi uygulanarak doğrusal olmayan (non-linear) filtrelemenin gürültü temizleme başarısı ve PSNR artışı incelenmiştir.

---

## 1. Yöntem ve Teorik Altyapı

### A. Medyan Filtresi Prensibi
Tuz ve biber gürültüsü pikselleri genellikle ekstrem parlaklık değerlerine (0 veya 255) sahiptir. Ortalama (mean) filtresi bu uç değerleri yumuşatarak çevreye yayarken, **medyan filtresi** pencere içerisindeki değerleri sıralayıp ortadaki değeri seçtiği için aykırı (outlier) değerleri tamamen eler:

$$
I_{\text{çıkış}}(x, y) = \text{medyan} \{ I(x+i, y+j) \mid -2 \le i, j \le 2 \}
$$

### B. Vektörize Sıralama Ağı (Sorting Network)
$5 \times 5 = 25$ piksellik pencere katmanları karşılaştırma sıralamasıyla (minimum/maximum takasları) vektörize edilerek tüm matris için tek seferde hesaplanmış ve 13. eleman (medyan) doğrudan filtrelenmiş görüntü matrisi olarak elde edilmiştir.

### C. Kenar Yönetimi
OpenCV `cv2.medianBlur` fonksiyonu ile uyumluluk amacıyla kenar sınırlarında `BORDER_REPLICATE` (en yakın sınır pikselini kopyalama) yaklaşımı uygulanmıştır.

---

## 2. Sonuçlar ve Doğrulama

| Görüntü | Tuz-Biber PSNR (dB) | Medyan Filtreli PSNR (dB) | PSNR Kazancı (dB) | OpenCV Farkı (Maks / SAD) |
| :--- | :---: | :---: | :---: | :---: |
| **dag** | 14.55 dB | **45.82 dB** | **+31.26 dB** | 0 / 0 (Birebir Eşleşme) |
| **sis** | 14.66 dB | **36.12 dB** | **+21.46 dB** | 0 / 0 (Birebir Eşleşme) |

Medyan filtresi, tuz-biber gürültüsünde ortalama filtresine kıyasla olağanüstü yüksek bir sinyal iyileştirme (+31 dB) sağlayarak kenar keskinliğini korumuştur.

---

## 3. Çalıştırma

```bash
python3 main.py
```
Çıktı görselleri ve sayısal rapor `cikti/` klasörüne kaydedilir.
