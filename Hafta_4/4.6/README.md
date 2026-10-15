# Ödev 4.6: 7x7 Analitik LoG (Laplacian of Gaussian) Kenar Tespiti

Bu ödevde, Gauss yumuşatma ile 2. mertebeden Laplacian türevini analitik formülde birleştiren **$7 \times 7$ LoG** operatörü sıfırdan üretilmiş ve sıfır geçişi (zero-crossing) ile kenar haritası çıkarılmıştır.

---

## 1. Yöntem ve Matematiksel Altyapı

LoG çekirdeği analitik türev formülü:

$$
\text{LoG}(x, y) = \frac{r^2 - 2\sigma^2}{\sigma^4} \exp\left(-\frac{r^2}{2\sigma^2}\right), \quad r^2 = x^2 + y^2
$$

- $\sigma = 1.0$ için $x, y \in \{-3, -2, -1, 0, 1, 2, 3\}$ koordinatlarında $7 \times 7$ çekirdek hesaplanır.
- Düzgün (homojen) alanlarda sıfır tepki vermesi için çekirdek ortalaması $0$'a çekilir: $K = K - \text{mean}(K)$.
- Enerji korunumu için mutlak toplamı $1.0$'a normalize edilir: $K = K / \sum |K_{i,j}|$.
- LoG çekirdeği yapısında Gauss yumuşatmasını barındırdığı için **harici bir ön filtreleme gerektirmez**.

---

## 2. Çıktılar

- `cikti/kamera_log_isaretli.png`: Normalize edilmiş işaretli LoG yanıtı.
- `cikti/kamera_log_mutlak.png`: LoG mutlak genlik haritası.
- `cikti/kamera_log_ikili.png`: 8-komşuluklu sıfır geçişi ikili kenar haritası.
- `cikti/panel_log.png`: 4 adımlı görsel analiz panosu.

---

## 3. Çalıştırma

```bash
python3 main.py
```
