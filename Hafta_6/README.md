# 📂 Hafta 6: Hough Dönüşümleri (Doğru, Çember, Eş Merkezli Çemberler ve CUDA)

Bu klasör, Görüntü İşleme dersinin 6. haftasına ait tüm ödevleri içerir.

| Ödev Kodu | Konu | Betik | Çıktılar / Rapor |
| :---: | :--- | :--- | :--- |
| **6.1** | **OpenCV HoughLines ve HoughLinesP ile Doğru Tespiti**<br>• Canny + 3x3 medyan filtreleme<br>• Standart Hough (13 doğru) ve Olasılıksal Hough (31 doğru parçası) | [`main.py`](6.1/main.py) | `cikti/dogrular_houghlines.png`<br>`cikti/dogrular_houghlinesp.png`<br>`cikti/rapor.txt` |
| **6.2** | **Özel Hough Doğru Dönüşümü ve Oylama Matrisi**<br>• $\rho = x\cos\theta + y\sin\theta$ formülüyle sıfırdan akümülatör<br>• Inferno ısı haritası ve NMS ile 14 tepe tespiti | [`main.py`](6.2/main.py) | `cikti/oylama_matrisi.png`<br>`cikti/dogrular_kendi.png`<br>`cikti/rapor.txt` |
| **6.3** | **OpenCV HoughCircles ile Çember Tespiti**<br>• Canny + medyan ve `HOUGH_GRADIENT`<br>• Smarties şekerlerinin merkez ve yarıçap tespiti (12 çember) | [`main.py`](6.3/main.py) | `cikti/cemberler_houghcircles.png`<br>`cikti/rapor.txt` |
| **6.4** | **Özel 3 Boyutlu Hough Çember Dönüşümü**<br>• $[y, x, r]$ 3B akümülatör matrisinde sıfırdan oylama<br>• Oy/çevre normalizasyonu ve 2B izdüşüm ısı haritası (12 çember) | [`main.py`](6.4/main.py) | `cikti/oylama_matrisi_merkezler.png`<br>`cikti/cemberler_kendi.png`<br>`cikti/rapor.txt` |
| **6.5** | **Gradyan Yönlü Eş Merkezli Çember Tespiti**<br>• Sobel normali doğrultusunda merkez oylaması<br>• Aynı sütundaki çoklu tepelerle eş merkezli 2 küme ([21,46,71] ve [36,66,96]) | [`main.py`](6.5/main.py) | `cikti/oylama_merkez_skoru.png`<br>`cikti/cemberler_es_merkezli.png`<br>`cikti/rapor.txt` |
| **6.6** | **CUDA ile Paralel Hough Line Oylaması**<br>• `hough_line.cu` CUDA C çekirdeği ve atomicAdd senkronizasyonu<br>• CPU ile mutlak fark = 0 doğrulama ve 37x - 62x GPU hızlanması | [`main.py`](6.6/main.py)<br>[`hough_line.cu`](6.6/hough_line.cu) | `cikti/dogrular_cuda.png`<br>`cikti/test.txt` |
