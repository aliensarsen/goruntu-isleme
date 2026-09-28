# Ödev 2.2: Görüntüyü 4 Parçaya Bölüp Thread'ler ile İşleme

Bu ödevde gri seviyeli bir görüntü 4 eşit kadrana bölünmüş ve her parçaya farklı bir nokta işlemi (artırma, azaltma, negatif alma, gamma eğrisi) uygulanmıştır.

## İşlemler
- **1. Bölge (Sol Üst):** $x + 50$ (Aydınlatma)
- **2. Bölge (Sağ Üst):** $x - 50$ (Karartma)
- **3. Bölge (Sol Alt):** $255 - x$ (Görüntü Negatifi)
- **4. Bölge (Sağ Alt):** $\sqrt{x/255} \cdot 255$ ($\gamma = 0.5$ Doğrusal Olmayan Dönüşüm)

## Çalıştırma
```bash
python3 main.py
```

## Üretilen Çıktılar
- `cikti/parca_sonuc.png`: 4 parçanın işlenip tekrar birleştirildiği sonuç görseli.
- `cikti/parca_thread_cikti.txt`: 1 thread ve 4 thread süre karşılaştırma raporu.
