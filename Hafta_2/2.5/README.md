# Ödev 2.5: Parlaklık ve Kontrast Dönüşümü ($y = 0.75 \cdot x + 20$)

Bu ödevde, gri seviyeli bir görüntüye doğrusal nokta dönüşümü uygulanarak çarpanın (kontrast) ve toplamanın (parlaklık) etkileri hem ayrı ayrı hem de birlikte gözlemlenmiştir.

## Matematiksel İfade
- **Kontrast Daraltma:** $y_1 = 0.75 \cdot x$
- **Parlaklık Artırma:** $y_2 = x + 20$
- **Birlikte Dönüşüm:** $y_3 = 0.75 \cdot x + 20$

## Çalıştırma
```bash
python3 main.py
```

## Üretilen Çıktılar
- `cikti/carp_075.png`: Yalnızca kontrastı düşürülmüş görüntü.
- `cikti/topla_20.png`: Yalnızca parlaklığı artırılmış görüntü.
- `cikti/donusum.png`: $0.75 \cdot x + 20$ dönüşümlü görüntü.
- `cikti/karsilastirma.png`: 4 görüntüyü bir arada gösteren 2x2 karşılaştırma paneli.
- `cikti/parlaklik_donusum_cikti.txt`: İstatistiksel ölçüm raporu.
