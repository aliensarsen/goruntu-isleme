# 📂 Hafta 7: Renk Uzayları, Görüntü Formatları ve Dönüşüm Analizi

Bu klasör, Görüntü İşleme dersinin 7. haftasına ait laboratuvar ve uygulama ödevlerini içerir.

| Ödev Kodu | Konu | Betik | Çıktılar / Rapor |
| :---: | :--- | :--- | :--- |
| **7.1** | **Renk Uzayları Araştırması ve 1000x1000 BMP Boyut / Kanal Analizi**<br>• RGB, HSV, YUV, CIE L\*a\*b\*, Grayscale, CMYK kuramsal incelemesi<br>• 24-bit $1000 \times 1000$ renkli BMP $\rightarrow$ 8-bit gri seviye BMP dönüşümü<br>• DIB/BMP başlıkları, 1024 baytlık renk paleti ve kanal sayısı kıyaslaması ($3{,}000{,}054$ bayt vs $1{,}001{,}078$ bayt) | [`main.py`](7.1/main.py)<br>[`README.md`](7.1/README.md) | `cikti/gri_1000x1000.bmp`<br>`cikti/boyut_analizi_raporu.txt`<br>`cikti/karsilastirma_gorsel.png`<br>`cikti/renk_uzaylari_karsilastirma.png` |
| **7.2** | **8K Çözünürlükte 3-Kanallı BMP Düzenleme ve Hassas Süre Ölçümü**<br>• 8K UHD ($7680 \times 4320 \times 3$) 24-bit BMP görüntüsü ($99{,}532{,}854$ bayt)<br>• OpenCV ile açma; piksel değerlerini 2'ye bölme (`img // 2`, `>> 1`, in-place, `cv2.divide`, threading)<br>• Dosya açma/kaydetme hariç yalnız düzenleme süresi (8.67 ms / 10.69 GB/sn) | [`main.py`](7.2/main.py)<br>[`README.md`](7.2/README.md) | `cikti/8k_duzenlenmis.bmp`<br>`cikti/sure_ve_performans_raporu.txt`<br>`cikti/8k_karsilastirma_ve_sure.png`<br>`cikti/8k_onizleme_*.jpg` |
| **7.3** | **Renk Uzayları Dönüşümü (HSV, HSI, YUV, CIE Lab) ve BMP Kaydetme**<br>• RGB BMP görüntüsünün HSV, HSI, YUV, CIE L\*a\*b\* uzaylarına dönüştürülmesi<br>• Sıfırdan Gonzalez & Woods formülüyle HSI fonksiyonu ($I = (R+G+B)/3$)<br>• Her bir uzayın 3-kanallı 24-bit BMP olarak kaydedilmesi ve 5x4 ızgara paneli | [`main.py`](7.3/main.py)<br>[`README.md`](7.3/README.md) | `cikti/resim_hsv.bmp`<br>`cikti/resim_hsi.bmp`<br>`cikti/resim_yuv.bmp`<br>`cikti/resim_cielab.bmp`<br>`cikti/renk_uzaylari_paneli.png`<br>`cikti/donusum_raporu.txt` |

---

## 🚀 Hızlı Başlangıç

```bash
# 7.1 Ödevi:
cd Hafta_7/7.1 && python3 main.py

# 7.2 Ödevi (8K Düzenleme ve Süre Ölçümü):
cd Hafta_7/7.2 && python3 main.py

# 7.3 Ödevi (HSV, HSI, YUV, CIE Lab BMP Dönüşümleri):
cd Hafta_7/7.3 && python3 main.py
```
