#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 4.5 (4. Hafta 5. Ödev)
KONU  : 3x3 Laplacian 2. Mertebe İzotropik Kenar Tespiti ve Sıfır Geçişi Analizi
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Girdi kamera görüntüsüne Gauss'lu ve Gauss'suz 3x3 Laplacian operatörünü uygular.
 2. 8-komşuluklu sıfır geçişi (zero-crossing) ile ikili kenar haritalarını üretir.
 3. İkinci türevin gürültüye aşırı duyarlılığını ve Gauss yumuşatmanın etkisini görselleştirir.
 4. 2x3 panel (panel_laplacian.png) ve karşılaştırma raporunu kaydeder.
"""

from pathlib import Path
import sys
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA4_DIR = KLASOR.parent
sys.path.insert(0, str(HAFTA4_DIR))

from kenarlar import (
    gauss_yumusat,
    isaretli_goruntu_uint8,
    laplacian,
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

    # 1. Laplacian (Gauss'suz) - Gürültü duyarlılığı
    lap_no = laplacian(gri, yumusat=False)
    lap_no_vis = isaretli_goruntu_uint8(lap_no)
    lap_no_zc = sifir_gecis(lap_no, esik_orani=0.05)

    # 2. Laplacian (Gauss'lu) - Filtrelenmiş 2. türev
    lap_gauss = laplacian(gri, yumusat=True)
    lap_gauss_vis = isaretli_goruntu_uint8(lap_gauss)
    lap_gauss_zc = sifir_gecis(lap_gauss, esik_orani=0.05)

    # 3. Görsel Karşılaştırma Paneli (2x3)
    panel = panel_olustur(
        [gri, lap_no_vis, lap_no_zc, gauss_yumusat(gri), lap_gauss_vis, lap_gauss_zc],
        [
            "1. Girdi (Orijinal)",
            "2. Laplacian (Gauss'suz Isaretli)",
            "3. Sifir Gecisi (Gauss'suz)",
            "4. 5x5 Gauss Yumusatma",
            "5. Laplacian (Gauss'lu Isaretli)",
            "6. Sifir Gecisi (Gauss'lu)",
        ],
        (2, 3),
    )

    cv2.imwrite(str(cikti_klasor / "kamera_laplacian_no_ikili.png"), lap_no_zc)
    cv2.imwrite(str(cikti_klasor / "kamera_laplacian_gauss_ikili.png"), lap_gauss_zc)
    cv2.imwrite(str(cikti_klasor / "kamera_laplacian_isaretli.png"), lap_gauss_vis)
    cv2.imwrite(str(cikti_klasor / "panel_laplacian.png"), panel)

    no_kenar = int(np.count_nonzero(lap_no_zc))
    gauss_kenar = int(np.count_nonzero(lap_gauss_zc))

    rapor = (
        "============================================================\n"
        "Ödev 4.5: 3x3 Laplacian ve Sıfır Geçişi Raporu\n"
        "============================================================\n\n"
        f"Görüntü Boyutu                 : {gri.shape[1]}x{gri.shape[0]}\n"
        f"Gauss'suz Sıfır Geçişi Kenarları: {no_kenar} piksel (Gürültü baskın)\n"
        f"Gauss'lu Sıfır Geçişi Kenarları : {gauss_kenar} piksel (Anlamlı hatlar)\n"
        f"Gürültü Eleme Oranı            : %{(1 - gauss_kenar / max(no_kenar, 1)) * 100:.2f}\n"
    )

    with open(cikti_klasor / "rapor.txt", "w", encoding="utf-8") as f:
        f.write(rapor)

    print(rapor)
    print("✓ Ödev 4.5 tamamlandı.")


if __name__ == "__main__":
    main()
