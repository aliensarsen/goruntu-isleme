# Ödev 6.5: Gradyan Yönlü Oylama ile Özel Eş Merkezli Çember Tespiti

Bu ödevde, aynı merkezi paylaşan eş merkezli çemberleri (concentric circles) doğrudan parametre uzayında tespit eden gradyan yönlü Hough algoritması geliştirilmiştir.

---

## 1. Yöntem ve Kuramsal Temel

1. **Gradyan Yönü (Kenar Normali):** Bir çember üzerindeki her noktanın kenar normali (Sobel gradyan doğrultusu) doğrudan çember merkezinden geçer:
   $$\theta_{\text{normal}} = \arctan\left(\frac{G_y}{G_x}\right)$$
2. **Kısıtlı Oylama (Gradient-Directed Voting):** Standart çember Hough'unda her piksel 360 açıda oy verirken, bu yöntemde piksel yalnızca kendi gradyan doğrultusunda ($\pm 2^\circ$ toleransla) oy kullanır.
3. **Eş Merkezli Kümelerin Yakalanması:** Aynı merkeze sahip iç içe geçmiş halkaların tamamı akümülatörün aynı $(a, b)$ sütununa oy verir. Sütun boyunca $r$ ekseninde birden fazla tepe tespit edildiğinde bu merkez doğrudan eş merkezli bir küme olarak sınıflandırılır.

---

## 2. Çıktılar

- `cikti/kenar_canny.png`: Canny kenar haritası.
- `cikti/oylama_merkez_skoru.png`: Akümülatörün $(a, b)$ sütunlarındaki toplam oy skoru ısı haritası.
- `cikti/cemberler_es_merkezli.png`: Eş merkezli çemberlerin farklı renklerle çizildiği sonuç görseli.
- `cikti/rapor.txt`: Bulunan merkezler, halka sayıları ve yarıçap değerleri.

---

## 3. Çalıştırma

```bash
python3 main.py
```
