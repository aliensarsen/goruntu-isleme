# Ödev 4.7: OpenCV Canny ve Tüm Kenar Yöntemlerinin Kapsamlı Başarım Analizi

Bu ödevde, çok adımlı gelişmiş kenar tespit algoritması olan **Canny Edge Detector** uygulanmış; Prewitt, Sobel, Laplacian, LoG ve Canny algoritmaları çalışma süresi (ms) ile zemin gerçeği (ground truth) bilinen sentetik ve gürültülü görüntüler üzerinde Precision, Recall ve F1-skor metrikleriyle kıyaslanmıştır.

---

## 1. Canny Algoritması Aşamaları

1. **Gauss Filtreleme:** Gürültüyü bastırmak için $5 \times 5$ ($\sigma=1.0$) filtreleme.
2. **Gradyan Hesabı:** $S_x$ ve $S_y$ Sobel çekirdekleriyle türev ve yön açısı $\theta = \arctan(G_y / G_x)$.
3. **Non-Maximum Suppression (NMS):** Gradyan yönünde yerel maksimum olmayan pikselleri sıfırlayarak kenarları 1 piksel kalınlığa inceltme.
4. **Histerezis Eşikleme (Çift Eşik):**
   - $T_{\text{high}} = 100$: Kesin kenarlar.
   - $T_{\text{low}} = 50$: Kesin kenarlara bağlı olan zayıf kenarlar dahil edilir, bağımsız gürültüler elenir.

---

## 2. Kapsamlı Ölçüm ve Karşılaştırma Sonuçları

Aşağıdaki ölçümler 15 tekrar medyanı olarak hesaplanmıştır (1 piksel toleranslı):

| Test Görüntüsü | Yöntem | Gauss Yumuşatma | Süre (ms) | Precision | Recall | F1-Score |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **kamera** | Prewitt | Evet | 1.18 ms | — | — | — |
| **kamera** | Sobel | Evet | 0.92 ms | — | — | — |
| **kamera** | Laplacian | Evet | 3.69 ms | — | — | — |
| **kamera** | LoG (7x7) | Dahili | 4.04 ms | — | — | — |
| **kamera** | Canny | Evet | **0.93 ms** | — | — | — |
| **sentetik** | Prewitt | Hayır | 0.77 ms | 1.0000 | 1.0000 | **1.0000** |
| **sentetik** | Sobel | Hayır | 0.74 ms | 1.0000 | 1.0000 | **1.0000** |
| **sentetik** | Canny | Evet | **0.30 ms** | 1.0000 | 1.0000 | **1.0000** |
| **sentetik_gurultulu** | Prewitt | Evet | 0.93 ms | 0.8759 | 1.0000 | 0.9338 |
| **sentetik_gurultulu** | Sobel | Evet | 0.91 ms | 0.8779 | 1.0000 | 0.9350 |
| **sentetik_gurultulu** | Laplacian | Evet | 4.09 ms | 0.0209 | 0.9996 | 0.0410 |
| **sentetik_gurultulu** | LoG | Dahili | 4.55 ms | 0.0196 | 1.0000 | 0.0385 |
| **sentetik_gurultulu** | **Canny** | **Evet** | **0.32 ms** | **1.0000** | **1.0000** | **1.0000** |

---

## 3. Bulgular ve Yorum

- **En Başarılı Algoritma:** Gürültülü sahnede Canny algoritması histerezis eşiklemesi ve NMS sayesinde sahte kenarları tamamen filtrelemiş ve **1.0000 F1 skorunu** korumayı başarmıştır.
- **İkinci Türev Zafiyeti:** Laplacian ve LoG yöntemleri gürültülü senaryoda aşırı duyarlılık nedeniyle çok sayıda sahte kenar üretmiş ve F1 skoru $< 0.05$ seviyesine gerilemiştir.
- **Çalışma Hızı:** Canny, OpenCV'nin C++ SIMD optimize çekirdeği sayesinde 0.32 ms gibi son derece yüksek bir işlem hızına ulaşmıştır.

---

## 4. Çalıştırma

```bash
python3 main.py
```
Çıktı görselleri ve `olcumler.csv` tablosu `cikti/` klasörüne kaydedilir.
