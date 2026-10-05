# Ödev 3.4: 3x3 Ortalama (Mean/Box) Filtresi ile Gürültü Temizleme ve PSNR Analizi

Bu ödevde, Gauss gürültüsü içeren gri tonlamalı görüntülere 3x3 ortalama (mean/box) filtresi uygulanarak gürültünün bastırılması ve orijinal temiz görüntüye göre Tepe Sinyal-Gürültü Oranı (PSNR - Peak Signal-to-Noise Ratio) artışı incelenmiştir.

---

## 1. Yöntem ve Matematiksel Altyapı

### A. 3x3 Ortalama Çekirdeği
Ortalama filtresi, bir pikselin ve etrafındaki 8 komşusunun aritmetik ortalamasını alarak yeni piksel değerini belirler. Çekirdek (kernel):

$$
K = \frac{1}{9} \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}
$$

### B. Kenar Koşulları
Kenar pikselleri için OpenCV'nin varsayılan sınır yansıtma (`cv2.BORDER_REFLECT_101`) stratejisi uygulanmıştır.

### C. PSNR (Peak Signal-to-Noise Ratio)
Ortalama Karesel Hata (MSE) ve PSNR formülleri:

$$
\text{MSE} = \frac{1}{M \cdot N} \sum_{i=0}^{M-1} \sum_{j=0}^{N-1} (I_{\text{temiz}}(i, j) - I_{\text{test}}(i, j))^2
$$

$$
\text{PSNR} = 10 \cdot \log_{10}\left(\frac{255^2}{\text{MSE}}\right) \quad (\text{dB})
$$

---

## 2. Sonuçlar ve Doğrulama

| Görüntü | Gürültülü PSNR (dB) | Filtreli PSNR (dB) | PSNR Artışı (dB) | OpenCV Farkı (Maks / SAD) |
| :--- | :---: | :---: | :---: | :---: |
| **dag** | 22.37 dB | **31.70 dB** | **+9.33 dB** | 0 / 0 (Birebir Eşleşme) |
| **sis** | 22.56 dB | **31.00 dB** | **+8.44 dB** | 0 / 0 (Birebir Eşleşme) |

---

## 3. Çalıştırma

```bash
python3 main.py
```
Çıktı görselleri ve sayısal rapor `cikti/` klasörüne kaydedilir.
