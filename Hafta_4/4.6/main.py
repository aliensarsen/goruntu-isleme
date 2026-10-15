#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 4.6 (4. Hafta 6. Ödev)
KONU  : 7x7 Analitik LoG (Laplacian of Gaussian) Kenar Tespiti
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. 7x7 analitik LoG çekirdeğini (sigma=1.0) formülünden üretir.
 2. Çekirdek ortalamasını 0 yapar ve mutlak toplamı 1'e normalize eder.
 3. Girdi kamera görüntüsüne tek konvolüsyonla LoG filtresini uygular.
 4. İşaretli, mutlak ve 8-komşuluklu sıfır geçişi (zero-crossing) ikili kenar haritalarını çıkarır.
 5. Karşılaştırma paneli (panel_log.png) ve raporunu kaydeder.
"""

from pathlib import Path
import sys
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA4_DIR = KLASOR.parent
sys.path.insert(0, str(HAFTA4_DIR))

from kenarlar import (
    isaretli_goruntu_uint8,
    log_cekirdegi,
    log_filtresi,
    mutlak_uint8,
    panel_olustur,
    sifir_gecis,
)


def main():
    cikti_klasor = KLASOR / "cikti"
    cikti_klasor.mkdir(parents=True, exist_ok=True)

    girdi_yol = HAFTA4_DIR / "girdi" / "kamera.png"
    if not girdi_yol.exists():
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {girdi_yol}")

    gri = cv2.imread(str(girdi_yol), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise ValueError("kamera.png okunamadı!")

    # 1. 7x7 Analitik LoG
    log_res = log_filtresi(gri)
    log_vis = isaretli_goruntu_uint8(log_res)
    log_abs = mutlak_uint8(log_res)
    log_zc = sifir_gecis(log_res, esik_orani=0.05)

    # 2. Panel: 1x4 Grid
    panel = panel_olustur(
        [gri, log_vis, log_abs, log_zc],
        [
            "1. Girdi (Orijinal)",
            "2. 7x7 LoG (Isaretli)",
            "3. 7x7 LoG (Mutlak Genlik)",
            "4. LoG Sifir Gecisi (Ikili Kenar)",
        ],
        (1, 4),
    )

    cv2.imwrite(str(cikti_klasor / "kamera_log_isaretli.png"), log_vis)
    cv2.imwrite(str(cikti_klasor / "kamera_log_mutlak.png"), log_abs)
    cv2.imwrite(str(cikti_klasor / "kamera_log_ikili.png"), log_zc)
    cv2.imwrite(str(cikti_klasor / "panel_log.png"), panel)

    kenar_sayisi = int(np.count_nonzero(log_zc))
    cekirdek = log_cekirdegi()

    rapor = (
        "============================================================\n"
        "Ödev 4.6: 7x7 Analitik LoG Kenar Tespiti Raporu\n"
        "============================================================\n\n"
        f"Çekirdek Boyutu       : 7x7 (sigma=1.0)\n"
        f"Çekirdek Ortalaması   : {float(cekirdek.mean()):.6e} (~0)\n"
        f"Çekirdek Mutlak Toplam: {float(np.sum(np.abs(cekirdek))):.4f} (1.0000)\n"
        f"Merkez Eleman Değeri  : {float(cekirdek[3, 3]):.4f} (Negatif tepe)\n"
        f"Görüntü Boyutu        : {gri.shape[1]}x{gri.shape[0]}\n"
        f"Sıfır Geçişi Kenarları : {kenar_sayisi} piksel\n"
    )

    with open(cikti_klasor / "rapor.txt", "w", encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print("✓ Ödev 4.6 tamamlandı.")


if __name__ == "__main__":
    main()
