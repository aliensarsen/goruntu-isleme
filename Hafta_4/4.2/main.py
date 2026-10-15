#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 4.2 (4. Hafta 2. Ödev)
KONU  : Prewitt Y Gradyan Operatörü ile Yatay Kenar Tespiti
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. Girdi kamera görüntüsüne 5x5 Gauss yumuşatma (sigma=1.0) uygular.
 2. [[-1, -1, -1], [0, 0, 0], [1, 1, 1]] Prewitt Y çekirdeğini konvolüsyonla uygular.
    Gy, düşey yoğunluk değişimini ölçtüğünden yatay kenarlara yüksek tepki verir.
 3. İşaretli float32 türevi 0-255 aralığına normalize ederek uint8 olarak görselleştirir.
 4. Orijinal, yumuşatılmış ve kenar haritasından oluşan panel görselini kaydeder.
"""

from pathlib import Path
import sys
import cv2
import numpy as np

KLASOR = Path(__file__).resolve().parent
HAFTA4_DIR = KLASOR.parent
sys.path.insert(0, str(HAFTA4_DIR))

from kenarlar import gauss_yumusat, isaretli_goruntu_uint8, panel_olustur


def prewitt_y(gri: np.ndarray) -> np.ndarray:
    """Prewitt Y çekirdeği ile yatay kenarları tespit eder (işaretli float32 döner)."""
    ky = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    girdi_f = gri.astype(np.float32, copy=False)
    return cv2.filter2D(girdi_f, cv2.CV_32F, ky, borderType=cv2.BORDER_REFLECT_101)


def main():
    cikti_klasor = KLASOR / "cikti"
    cikti_klasor.mkdir(parents=True, exist_ok=True)

    girdi_yol = HAFTA4_DIR / "girdi" / "kamera.png"
    if not girdi_yol.exists():
        raise FileNotFoundError(f"Girdi dosyası bulunamadı: {girdi_yol}")

    gri = cv2.imread(str(girdi_yol), cv2.IMREAD_GRAYSCALE)
    if gri is None:
        raise ValueError("kamera.png okunamadı!")

    # 1. 5x5 Gauss Yumuşatma (sigma=1.0)
    yumusak = gauss_yumusat(gri)

    # 2. Prewitt Y Türevi (Gy)
    gy = prewitt_y(yumusak)
    gy_vis = isaretli_goruntu_uint8(gy)

    # 3. Görsel Panel: Girdi / Yumuşatılmış / Prewitt Y Sonuç
    panel = panel_olustur(
        [gri, yumusak, gy_vis],
        ["1. Girdi (Orijinal Gri)", "2. 5x5 Gauss Yumusatma", "3. Prewitt Y (Yatay Kenar Sonucu)"],
        (1, 3),
    )

    cv2.imwrite(str(cikti_klasor / "kamera_gauss.png"), yumusak)
    cv2.imwrite(str(cikti_klasor / "kamera_prewitt_gy.png"), gy_vis)
    cv2.imwrite(str(cikti_klasor / "panel_prewitt_y.png"), panel)

    print("✓ Ödev 4.2 (Prewitt Y) başarıyla tamamlandı.")


if __name__ == "__main__":
    main()
