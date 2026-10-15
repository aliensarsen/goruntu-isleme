# Ödev 4.5: 3x3 Laplacian 2. Mertebe Kenar Tespiti ve Sıfır Geçişi

Bu ödevde, yön bağımsız (izotropik) 2. mertebeden türev operatörü olan **3x3 Laplacian** uygulanmış ve kenarların sıfır geçişi (zero-crossing) ile tespiti incelenmiştir.

---

## 1. Yöntem ve Matematiksel Altyapı

Laplacian operatörü tüm yönlerdeki ikinci türevlerin toplamıdır:

$$
\nabla^2 I = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}
$$

4-komşuluklu çekirdek:

$$
K_{\text{Lap}} = \begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
$$

### Sıfır Geçişi (Zero-Crossing) Prensibi
Kenar geçişinde fonksiyonun 1. türevi tepe yaparken, 2. türevi sıfırdan geçer ($+ \rightarrow -$ veya $- \rightarrow +$). 8-komşuluklu sıfır geçişi algoritması ile bu geçiş noktaları kenar çizgisi olarak işaretlenir.

---

## 2. Gürültü Hassasiyeti ve Gauss Yumuşatma

2. mertebe türev yüksek frekanslı gürültüleri karesel oranda ($\omega^2$) kuvvetlendirdiği için, ön filtreleme yapılmadığında saf gürültü piksellerinde bile sahte sıfır geçişleri oluşur ($> 68.000$ sahte kenar pikseli). $5 \times 5$ Gauss filtresi uygulandığında sahte kenarlar elenir ve gerçek nesne konturları belirginleşir.

---

## 3. Çalıştırma

```bash
python3 main.py
```
