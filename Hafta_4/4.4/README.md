# Ödev 4.4: Prewitt ve Sobel Karşılaştırma Analizi

Bu ödevde, 1. mertebeden türev operatörleri olan **Prewitt** ve **Sobel** algoritmalarının kenar tespit başarımı, gürültü direnci ve kenar yoğunluğu karşılaştırılmıştır.

---

## 1. Yöntem ve Kuramsal Farklar

| Özellik | Prewitt Operatörü | Sobel Operatörü |
| :--- | :--- | :--- |
| **Çekirdek Katsayıları** | Düz katsayılar: $[-1, 0, 1]$ | Ağırlıklı katsayılar: $[-1, 0, 1]$ ve merkez $[-2, 0, 2]$ |
| **Yumuşatma Etkisi** | Eşit ağırlıklı ortalama | Yerel 1-2-1 üçgensel Gauss benzeri yumuşatma |
| **Gürültü Direnci** | Yüksek frekanslı gürültülere daha açık | Merkez ağırlıklandırma sayesinde gürültüye daha dirençli |
| **Hesaplama Yükü** | $O(N \cdot M)$ | $O(N \cdot M)$ (Modern donanımlarda fark ihmal edilebilir) |

---

## 2. Sonuçlar ve Metrikler

- **Görsel Panel:** `cikti/karsilastirma_prewitt_sobel.png`
- **Sayısal Rapor:** `cikti/rapor.txt`

Her iki yöntem de genel yapıları benzer biçimde yakalamakla birlikte, Sobel operatörü çapraz kenarlarda ve dokulu alanlarda daha dengeli ve pürüzsüz gradyan büyüklüğü sağlamaktadır.

---

## 3. Çalıştırma

```bash
python3 main.py
```
