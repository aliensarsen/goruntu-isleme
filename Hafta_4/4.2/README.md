# Ödev 4.2: Prewitt Y Gradyan Operatörü ile Yatay Kenar Tespiti

Bu ödevde, gri tonlamalı kameraman görüntüsüne $5 \times 5$ Gauss yumuşatma ($\sigma = 1.0$) uygulandıktan sonra **Prewitt Y** çekirdeği ile düşey türev ($G_y$) hesaplanmış ve yatay kenarlar tespit edilmiştir.

---

## 1. Yöntem ve Matematiksel Altyapı

Prewitt Y operatörü dikey eksendeki piksel farkını ölçer:

$$
K_y = \begin{bmatrix}
-1 & -1 & -1 \\
0 & 0 & 0 \\
1 & 1 & 1
\end{bmatrix}
$$

- $G_y = I * K_y$ konvolüsyonu sonucunda işaretli türev değerleri elde edilir.
- Yatay çizgi ve zemin geçişleri bu operatör altında en yüksek genliğe ulaşır.
- İşaretli float32 türevi negatifleri koruyacak şekilde 0-255 aralığına normalize edilmiştir.

---

## 2. Çıktılar

- `cikti/kamera_gauss.png`: $5 \times 5$ Gauss filtresi uygulanmış yumuşak görüntü.
- `cikti/kamera_prewitt_gy.png`: Normalize edilmiş $G_y$ yatay kenar yanıtı.
- `cikti/panel_prewitt_y.png`: Orijinal, yumuşatılmış ve yatay kenar kıyaslama paneli.

---

## 3. Çalıştırma

```bash
python3 main.py
```
