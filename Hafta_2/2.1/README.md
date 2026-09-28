# Ödev 2.1: 8-Bit Gri Görüntüyü 6-Bit Seviyesine Nicemleme (Quantization)

Bu ödevde, 8-bitlik derinliğe (256 farklı parlaklık seviyesi) sahip gri tonlamalı bir görüntü bit kaydırma yöntemi ile 6-bit derinliğe (64 seviye) nicemlenmiştir.

## Matematiksel Yaklaşım
- 8-bit piksel $x \in [0, 255]$ için alt 2 bit atılır:
  $$x_{\text{6bit}} = (x \gg 2) \ll 2$$
- Böylece her 4 bitişik gri seviyesi tek bir seviyede toplanır. Maksimum kuantalama hatası en fazla 3 seviyedir.

## Çalıştırma
```bash
python3 main.py
```

## Üretilen Çıktılar
- `cikti/gri.png`: Orijinal 8-bit gri seviye görsel.
- `cikti/6bit.png`: 64 seviyeli 6-bit nicemlenmiş görsel.
- `cikti/fark.png`: Kuantalama hatasını gösteren fark görseli.
- `cikti/nicemle_6bit_cikti.txt`: Ölçüm raporu.
