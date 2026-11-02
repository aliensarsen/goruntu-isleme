# Ödev 6.6: CUDA ile Paralel Hough Line Oylaması ve CPU Karşılaştırması

Bu ödevde, hesaplama karmaşıklığı $O(N_{\text{kenar}} \times N_\theta)$ olan Hough Line oylama adımı NVIDIA CUDA (C++/CUDA C) çekirdeği ile GPU üzerinde paralel hale getirilmiş ve CPU sürümüyle sayısal doğruluk ve çalışma hızı açısından kıyaslanmıştır.

---

## 1. Paralel Mimarisi ve CUDA Çekirdeği

- **İş Dağılımı:** Toplam $N_{\text{kenar}} \times 180$ bağımsız hesaplama işi, 256'şar iş parçacığından oluşan CUDA bloklarına dağıtılır.
- **Bellek Erişimi ve Atomik Toplama:** Birden çok GPU iş parçacığının aynı $(\rho, \theta)$ hücresine aynı anda yazmasını güvenli kılmak için `atomicAdd` fonksiyonu kullanılır.
- **Doğruluk (Eşleşme):** CPU tarafındaki `np.rint` yuvarlaması ile CUDA `rint` yuvarlama davranışı birebir örtüştürülmüş ve **fark toplamı 0** elde edilmiştir.

---

## 2. Başarım Ölçümleri (Benchmark)

| Test Senaryosu | Kenar Piksel Sayısı | CPU Süresi (ms) | GPU Süresi (ms) | Yalnızca Kernel | Hızlanma (Speedup) | Mutlak Hata |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sudoku (Medyan Filtreli)** | 7.129 | 120.7 ms | **3.3 ms** | 0.063 ms | **37x** | **0 (Birebir Eşit)** |
| **Sudoku (Canny Ham Kenar)** | 29.537 | 518.3 ms | **8.3 ms** | 0.201 ms | **62x** | **0 (Birebir Eşit)** |

GPU paralel çekirdeği, kenar piksel sayısı arttıkça hızlanma faktörünü **62 katına** çıkararak büyük çözünürlüklü görüntülerde gerçek zamanlı tespit olanağı sunmaktadır.

---

## 3. Çalıştırma ve Derleme

### CUDA DLL Derleme (Windows / Linux NVIDIA GPU)
```bash
nvcc -O2 -shared -o hough_line.dll hough_line.cu
```

### Python Testi
```bash
python3 main.py
```
