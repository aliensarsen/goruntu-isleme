# 📂 Hafta 2: Nicemleme, Threading ile Paralel İşleme ve Nokta Dönüşümleri

Bu klasör, Görüntü İşleme dersinin 2. haftasına ait tüm ödevleri içerir.

| Ödev Kodu | Konu | Betik | Çıktılar |
| :---: | :--- | :--- | :--- |
| **2.1** | **8-bit → 6-bit Nicemleme**<br>• Bit kaydırma ile 256 seviyeyi 64 seviyeye indirgeme<br>• Kuantalama hatasını gösteren fark görseli | [`main.py`](2.1/main.py) | `6bit.png`<br>`fark.png`<br>`nicemle_6bit_cikti.txt` |
| **2.2** | **4 Parça × 4 Thread Parlaklık İşlemleri**<br>• Görüntüyü 4 kadrana bölüp bağımsız dönüşümler uygulama<br>• 1 thread vs. 4 thread süre ölçümü | [`main.py`](2.2/main.py) | `parca_sonuc.png`<br>`parca_thread_cikti.txt` |
| **2.3** | **Parça Histogramları ve Birleştirme**<br>• 4 parça için thread ile histogram hesaplayıp toplama<br>• Tüm görüntü histogramı ile doğrulama (Fark = 0) | [`main.py`](2.3/main.py) | `histogram.png`<br>`histogram_thread_cikti.txt` |
| **2.4** | **Histogram Süre Kıyaslaması (1 Thread vs. 4 Thread)**<br>• 20 tekrar ile ortalama süre ve hızlanma ölçümü | [`main.py`](2.4/main.py) | `histogram_sure_cikti.txt` |
| **2.5** | **Parlaklık ve Kontrast Dönüşümü ($0.75 \cdot x + 20$)**<br>• Çarpma, toplama ve birleşik etkilerin analizi<br>• 2x2 karşılaştırma paneli | [`main.py`](2.5/main.py) | `carp_075.png`<br>`topla_20.png`<br>`donusum.png`<br>`karsilastirma.png` |
