# 📂 Hafta 4: Kenar Algoritmaları ve Gradyan Operatörleri

Bu klasör, Görüntü İşleme dersinin 4. haftasına ait tüm ödevleri içerir.

| Ödev Kodu | Konu | Betik | Çıktılar / Rapor |
| :---: | :--- | :--- | :--- |
| **4.1** | **Prewitt X Gradyan Operatörü**<br>• $5 \times 5$ Gauss yumuşatma ($\sigma=1.0$) ve Prewitt X çekirdeği<br>• Yatay türev ile düşey kenarların çıkarılması | [`main.py`](4.1/main.py) | `cikti/kamera_prewitt_gx.png`<br>`cikti/panel_prewitt_x.png` |
| **4.2** | **Prewitt Y Gradyan Operatörü**<br>• Prewitt Y çekirdeği ile düşey türev hesabı<br>• Yatay kenarların vurgulanması ve görselleştirilmesi | [`main.py`](4.2/main.py) | `cikti/kamera_prewitt_gy.png`<br>`cikti/panel_prewitt_y.png` |
| **4.3** | **3x3 Sobel Operatörü ve Gradyan Büyüklüğü**<br>• 3x3 Sobel türevleri ($G_x, G_y$), büyüklük ($|\nabla I|$) ve %20 dinamik eşikleme<br>• 2x3 kapsamlı analiz paneli | [`main.py`](4.3/main.py) | `cikti/kamera_sobel_hypot.png`<br>`cikti/kamera_sobel_ikili.png`<br>`cikti/panel_sobel.png` |
| **4.4** | **Prewitt ve Sobel Karşılaştırmalı Analizi**<br>• İki gradyan yönteminin büyüklük, eşik ve kenar yoğunluğu kıyası<br>• %97.90 benzerlik (IoU) ve fark matrisi analizi | [`main.py`](4.4/main.py) | `cikti/karsilastirma_prewitt_sobel.png`<br>`cikti/rapor.txt` |
| **4.5** | **3x3 Laplacian 2. Mertebe Kenar Tespiti**<br>• Yön bağımsız (izotropik) Laplacian 4-komşuluk çekirdeği<br>• 8-komşuluklu sıfır geçişi (zero-crossing) ve gürültü analizi | [`main.py`](4.5/main.py) | `cikti/kamera_laplacian_gauss_ikili.png`<br>`cikti/panel_laplacian.png` |
| **4.6** | **7x7 Analitik LoG (Laplacian of Gaussian)**<br>• $\sigma=1.0$ analitik formülünden sıfırdan $7 \times 7$ çekirdek üretimi<br>• Sıfır toplam ve mutlak normalizasyon ile tek adımda sıfır geçişi | [`main.py`](4.6/main.py) | `cikti/kamera_log_ikili.png`<br>`cikti/panel_log.png` |
| **4.7** | **OpenCV Canny ve Kapsamlı Başarım Analizi**<br>• Çok aşamalı Canny (NMS + histerezis 50/100)<br>• 9 varyant × 3 görüntü benchmark: Süre (ms), Precision, Recall, F1 tablosu | [`main.py`](4.7/main.py) | `cikti/olcumler.csv`<br>`cikti/karsilastirma_tum_yontemler.png` |
