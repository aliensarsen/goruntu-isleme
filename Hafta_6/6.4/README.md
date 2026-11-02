# Ödev 6.4: Özel 3 Boyutlu Hough Çember Dönüşümü

Bu ödevde, OpenCV'nin hazır fonksiyonları yerine $3$ boyutlu akümülatör matrisi ($y, x, r$) üzerinde çalışan özgün Hough çember dönüşümü algoritması geliştirilmiştir.

---

## 1. Yöntem ve Algoritmik Yapı

Çemberin parametrik denklemi:

$$
x = a + r \cos\theta, \quad y = b + r \sin\theta \implies a = x - r \cos\theta, \quad b = y - r \sin\theta
$$

1. **3B Akümülatör:** Boyutları $[H \times W \times R]$ olan matris tahsis edilir ($R = 21$, yarıçaplar $20 \dots 40$).
2. **Vektörize Oylama:** Her kenar pikseli için 360 açı ve 21 yarıçap kombinasyonundaki olası merkezler hesaplanıp akümülatöre 1 oy eklenir.
3. **Normalizasyon ve Eşikleme:**
   - Farklı yarıçaptaki çemberlerin çevre uzunlukları farklı olduğundan, oy sayısı çevreye bölünür: $\text{Oran} = \frac{\text{Oy}}{2\pi r}$.
   - $\text{Oran} \ge 0.20$ olan adaylar seçilir ve minimum merkez mesafesi ($20\text{ px}$) kısıtıyla yerel tekrarlar elenir.

---

## 2. Çıktılar

- `cikti/oylama_matrisi_merkezler.png`: 3B oylama uzayının $r$ eksenindeki maksimum izdüşüm ısı haritası.
- `cikti/cemberler_kendi.png`: Özgün algoritma ile bulunan çemberlerin (mor) ve merkezlerinin (kırmızı) çizildiği sonuç.
- `cikti/rapor.txt`: Bulunan çemberlerin merkezleri, yarıçapları ve oy/çevre oranları.

---

## 3. Çalıştırma

```bash
python3 main.py
```
