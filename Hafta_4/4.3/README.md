# Ödev 4.3: 3x3 Sobel Gradyan Operatörü, Büyüklük ve İkili Kenar Haritası

Bu ödevde, $512 \times 512$ gri seviye görüntüye $3 \times 3$ **Sobel** operatörü uygulanarak yatay ve dikey türevler, toplam gradyan büyüklüğü ve tepe değerin %20'si üzerinden ikili (binary) kenar haritası çıkarılmıştır.

---

## 1. Yöntem ve Matematiksel Altyapı

Sobel çekirdekleri merkez piksele 2 katsayısı vererek türev alırken yerel bir Gauss yumuşatması sağlar:

$$
S_x = \begin{bmatrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1
\end{bmatrix}, \quad
S_y = \begin{bmatrix}
-1 & -2 & -1 \\
0 & 0 & 0 \\
1 & 2 & 1
\end{bmatrix}
$$

### Gradyan Büyüklüğü (Euclidean Norm / Hypot)
Yön bağımsız kenar şiddeti:

$$
|\nabla I| = \sqrt{G_x^2 + G_y^2}
$$

### İkili Eşikleme
Dinamik eşikleme ile gürültü bastırılır ve belirgin kenarlar seçilir:

$$
\text{Edge}(x, y) = \begin{cases} 255, & \text{eğer } |\nabla I(x, y)| \ge 0.20 \cdot \max(|\nabla I|) \\ 0, & \text{diğer} \end{cases}
$$

---

## 2. Çıktılar

- `cikti/kamera_sobel_gx.png`: Düşey kenar türev haritası.
- `cikti/kamera_sobel_gy.png`: Yatay kenar türev haritası.
- `cikti/kamera_sobel_hypot.png`: Toplam gradyan büyüklüğü.
- `cikti/kamera_sobel_ikili.png`: %20 dinamik eşikleme sonucu ikili kenar görüntüsü.
- `cikti/panel_sobel.png`: 6 adımlı $2 \times 3$ analiz paneli.

---

## 3. Çalıştırma

```bash
python3 main.py
```
