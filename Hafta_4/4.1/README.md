# Ödev 4.1: Prewitt X Gradyan Operatörü ile Dikey Kenar Tespiti

Bu ödevde, $512 \times 512$ gri seviyeli kameraman görüntüsüne $5 \times 5$ Gauss yumuşatma ($\sigma = 1.0$) uygulandıktan sonra **Prewitt X** çekirdeği ile yatay türev ($G_x$) hesaplanmış ve dikey kenarlar ortaya çıkarılmıştır.

---

## 1. Yöntem ve Matematiksel Altyapı

Prewitt X operatörü yatay eksendeki piksel farkını ölçer:

$$
K_x = \begin{bmatrix}
-1 & 0 & 1 \\
-1 & 0 & 1 \\
-1 & 0 & 1
\end{bmatrix}
$$

- $G_x = I * K_x$ konvolüsyonu sonucunda işaretli türev değerleri elde edilir.
- Negatif türevlerin kırpılmaması için sonuç `cv2.normalize` ile $[0, 255]$ aralığına ölçeklenerek görselleştirilmiştir (0 türev nötr gri $\approx 128$, pozitif türev parlak, negatif türev karanlık).

---

## 2. Çıktılar

- `cikti/kamera_gauss.png`: $5 \times 5$ Gauss filtresi uygulanmış yumuşak görüntü.
- `cikti/kamera_prewitt_gx.png`: Normalize edilmiş $G_x$ dikey kenar yanıtı.
- `cikti/panel_prewitt_x.png`: Orijinal, yumuşatılmış ve kenar haritası kıyaslama paneli.

---

## 3. Çalıştırma

```bash
python3 main.py
```
