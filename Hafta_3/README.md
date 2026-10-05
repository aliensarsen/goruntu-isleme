# 📂 Hafta 3: Kontrast Germe, Histogram Eşitleme, CLAHE ve Uzamsal Filtreler

Bu klasör, Görüntü İşleme dersinin 3. haftasına ait tüm ödevleri içerir.

| Ödev Kodu | Konu | Betik | Çıktılar |
| :---: | :--- | :--- | :--- |
| **3.1** | **Min-Max Doğrusal Kontrast Germe**<br>• $[min, max] \rightarrow [0, 255]$ dinamik aralık genişletme<br>• Özel fonksiyon vs `cv2.normalize` | [`main.py`](3.1/main.py) | `cikti/dag_ozel.png`<br>`cikti/sis_ozel.png`<br>`cikti/rapor.txt` |
| **3.2** | **Histogram Eşitleme (Histogram Equalization)**<br>• Kümülatif Dağılım Fonksiyonu (CDF) ile normalize haritalama<br>• Özel CDF algoritması vs `cv2.equalizeHist` | [`main.py`](3.2/main.py) | `cikti/dag_ozel.png`<br>`cikti/sis_ozel.png`<br>`cikti/rapor.txt` |
| **3.3** | **CLAHE (Kontrast Sınırlı Adaptif Histogram Eşitleme)**<br>• 8x8 karolar üzerinde yerel kontrast iyileştirme<br>• Kırpma sınırı (clip limit) ve çift doğrusal enterpolasyon | [`main.py`](3.3/main.py) | `cikti/dag_ozel.png`<br>`cikti/sis_ozel.png`<br>`cikti/rapor.txt` |
| **3.4** | **3x3 Ortalama (Mean/Box) Filtresi**<br>• Gauss gürültüsünü 3x3 konvolüsyon çekirdeği ile yumuşatma<br>• PSNR kazancı analizi ve `cv2.blur` ile kıyaslama | [`main.py`](3.4/main.py) | `cikti/dag_ozel.png`<br>`cikti/sis_ozel.png`<br>`cikti/rapor.txt` |
| **3.5** | **5x5 Medyan Filtresi**<br>• Tuz-biber (salt & pepper) gürültüsünü doğrusal olmayan sıralama ile giderme<br>• +31 dB PSNR artışı ve `cv2.medianBlur` kıyası | [`main.py`](3.5/main.py) | `cikti/dag_ozel.png`<br>`cikti/sis_ozel.png`<br>`cikti/rapor.txt` |
