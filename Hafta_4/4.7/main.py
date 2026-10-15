#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 4.7 (4. Hafta 7. Ödev)
KONU  : OpenCV Canny Algoritması ve Tüm Kenar Yöntemlerinin Kapsamlı Başarım Analizi
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Canny kenar tespitini (çift eşikli histerezis 50/100, L2gradient) uygular.
 2. 9 farklı varyantı (Prewitt True/False, Sobel True/False, Laplacian True/False,
    LoG tek varyant, Canny True/False) 3 test görüntüsünde çalıştırır:
    - kamera (512x512)
    - sentetik (512x512 temiz geometrik)
    - sentetik_gurultulu (512x512 Gauss gürültülü, sigma=10)
 3. Her yöntem için medyan ms çalışma süresini ölçer.
 4. Sentetik zemin doğrusu (ground truth) ile Precision, Recall ve F1 skorlarını hesaplar.
 5. Sonuçları olcumler.csv dosyasına kaydeder ve 2x6'lık tüm yöntemler karşılaştırma paneli üretir.
"""

import csv
from pathlib import Path
import sys
import time
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA4_DIR = KLASOR.parent
sys.path.insert(0, str(HAFTA4_DIR))

from kenarlar import (
    canny,
    gradyan_ikili,
    kenar_skoru,
    laplacian,
    log_filtresi,
    prewitt,
    sentetik_veri_uret,
    sifir_gecis,
    sobel,
)


def sure_olc(fonksiyon, tekrar: int = 15, isinma: int = 3) -> float:
    """Fonksiyonun medyan çalışma süresini (ms) ölçer."""
    for _ in range(isinma):
        fonksiyon()
    sureler = []
    for _ in range(tekrar):
        t0 = time.perf_counter()
        fonksiyon()
        t1 = time.perf_counter()
        sureler.append((t1 - t0) * 1000.0)
    return float(np.median(sureler))


def main():
    cv2.setNumThreads(1)
    cikti_klasor = KLASOR / "cikti"
    cikti_klasor.mkdir(parents=True, exist_ok=True)

    girdi_yol = HAFTA4_DIR / "girdi" / "kamera.png"
    if not girdi_yol.exists():
        raise FileNotFoundError(f"Girdi bulunamadı: {girdi_yol}")

    kamera_img = cv2.imread(str(girdi_yol), cv2.IMREAD_GRAYSCALE)
    if kamera_img is None:
        raise ValueError("kamera.png okunamadı!")

    sentetik_img, ref_kenar, gurultulu_img = sentetik_veri_uret()

    # 9 Varyant Tanımı
    varyantlar = [
        ("Prewitt", False),
        ("Prewitt", True),
        ("Sobel", False),
        ("Sobel", True),
        ("Laplacian", False),
        ("Laplacian", True),
        ("LoG", True),
        ("Canny", False),
        ("Canny", True),
    ]

    test_goruntuleri = [
        ("kamera", kamera_img, None),
        ("sentetik", sentetik_img, ref_kenar),
        ("sentetik_gurultulu", gurultulu_img, ref_kenar),
    ]

    def yontem_calistir(img, yontem, yumusat):
        if yontem == "Prewitt":
            _, _, mag = prewitt(img, yumusat=yumusat)
            return gradyan_ikili(mag, esik_orani=0.2)
        elif yontem == "Sobel":
            _, _, mag = sobel(img, yumusat=yumusat)
            return gradyan_ikili(mag, esik_orani=0.2)
        elif yontem == "Laplacian":
            lap = laplacian(img, yumusat=yumusat)
            return sifir_gecis(lap, esik_orani=0.05)
        elif yontem == "LoG":
            log_res = log_filtresi(img)
            return sifir_gecis(log_res, esik_orani=0.05)
        elif yontem == "Canny":
            return canny(img, yumusat=yumusat)
        else:
            raise ValueError(f"Bilinmeyen yöntem: {yontem}")

    satirlar = []

    for g_ad, img, ref in test_goruntuleri:
        for yontem, yumusat in varyantlar:
            ms = sure_olc(lambda: yontem_calistir(img, yontem, yumusat))
            tahmin = yontem_calistir(img, yontem, yumusat)

            if ref is not None:
                p, r, f1 = kenar_skoru(tahmin, ref, tolerans=1)
                p_str = f"{p:.4f}"
                r_str = f"{r:.4f}"
                f1_str = f"{f1:.4f}"
            else:
                p_str = ""
                r_str = ""
                f1_str = ""

            satirlar.append({
                "goruntu": g_ad,
                "yontem": yontem,
                "yumusatma": str(yumusat),
                "sure_ms": f"{ms:.3f}",
                "precision": p_str,
                "recall": r_str,
                "f1": f1_str,
            })

    # CSV olarak kaydet
    csv_yol = cikti_klasor / "olcumler.csv"
    alanlar = ["goruntu", "yontem", "yumusatma", "sure_ms", "precision", "recall", "f1"]
    with open(csv_yol, "w", newline="", encoding="utf-8") as f:
        yazici = csv.DictWriter(f, fieldnames=alanlar)
        yazici.writeheader()
        yazici.writerows(satirlar)

    # Canny görsel çıktılarını kaydet
    kamera_canny_gauss = canny(kamera_img, yumusat=True)
    kamera_canny_nogauss = canny(kamera_img, yumusat=False)

    cv2.imwrite(str(cikti_klasor / "kamera_canny_gauss.png"), kamera_canny_gauss)
    cv2.imwrite(str(cikti_klasor / "kamera_canny_nogauss.png"), kamera_canny_nogauss)

    # 2x6 Karşılaştırma Paneli
    panel_gorseller = [
        kamera_img,
        gradyan_ikili(prewitt(kamera_img, True)[2]),
        gradyan_ikili(sobel(kamera_img, True)[2]),
        sifir_gecis(laplacian(kamera_img, True)),
        sifir_gecis(log_filtresi(kamera_img)),
        kamera_canny_gauss,
        gurultulu_img,
        gradyan_ikili(prewitt(gurultulu_img, True)[2]),
        gradyan_ikili(sobel(gurultulu_img, True)[2]),
        sifir_gecis(laplacian(gurultulu_img, True)),
        sifir_gecis(log_filtresi(gurultulu_img)),
        canny(gurultulu_img, yumusat=True),
    ]

    basliklar = [
        "Kamera Orijinal",
        "Prewitt (Kamera)",
        "Sobel (Kamera)",
        "Laplacian (Kamera)",
        "LoG (Kamera)",
        "Canny (Kamera)",
        "Gurultulu Sentetik",
        "Prewitt (Gurultulu)",
        "Sobel (Gurultulu)",
        "Laplacian (Gurultulu)",
        "LoG (Gurultulu)",
        "Canny (Gurultulu)",
    ]

    h, w = panel_gorseller[0].shape[:2]
    panel = np.full((2 * (h + 30), 6 * w, 3), 245, dtype=np.uint8)
    for idx, (img, b) in enumerate(zip(panel_gorseller, basliklar)):
        r = idx // 6
        c = idx % 6
        y0 = r * (h + 30)
        x0 = c * w
        cv2.rectangle(panel, (x0, y0), (x0 + w, y0 + 30), (40, 40, 40), -1)
        cv2.putText(panel, b, (x0 + 8, y0 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        img_b = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if len(img.shape) == 2 else img
        panel[y0 + 30 : y0 + h + 30, x0 : x0 + w] = img_b

    cv2.imwrite(str(cikti_klasor / "karsilastirma_tum_yontemler.png"), panel)

    print(f"✓ Ödev 4.7 tamamlandı. Toplam {len(satirlar)} ölçüm kaydedildi.")


if __name__ == "__main__":
    main()
