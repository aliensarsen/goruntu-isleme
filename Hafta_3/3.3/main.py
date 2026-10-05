#!/usr/bin/env python3
"""
======================================================================================
DERS  : Görüntü İşleme (EBLG351)
ÖDEV  : 3.3 (3. Hafta 3. Ödev)
KONU  : CLAHE (Contrast Limited Adaptive Histogram Equalization)
YAZAR : aliensarsen
======================================================================================

Bu betik:
 1. CLAHE algoritmasını clipLimit=2.0 ve tileGridSize=(8, 8) parametreleriyle uygular.
 2. Hem sıfırdan yazılmış karo bazlı kırpma/dağıtma/çift-doğrusal enterpolasyon (bilinear interpolation)
    fonksiyonuyla hem de cv2.createCLAHE ile çalıştırır.
 3. İki çıktıyı sayısal olarak karşılaştırır.
"""

from pathlib import Path
import cv2
import numpy as np

KLASOR = Path(__file__).parent
GIRDI_KLASOR = KLASOR.parent / "girdi"
CIKTI_KLASOR = KLASOR / "cikti"


def clahe_ozel(gri: np.ndarray, clip_limit: float = 2.0, karo: int = 8) -> np.ndarray:
    h, w = gri.shape
    pad_h = (karo - h % karo) % karo
    pad_w = (karo - w % karo) % karo

    if pad_h > 0 or pad_w > 0:
        genis = cv2.copyMakeBorder(gri, 0, pad_h, 0, pad_w, cv2.BORDER_REFLECT)
    else:
        genis = gri

    gh, gw = genis.shape
    kh = gh // karo
    kw = gw // karo
    alan = kh * kw
    limit = max(1, int(clip_limit * alan / 256.0))

    # 1. Karo bazlı eşitleme tabloları (LUTs)
    tablolar = np.zeros((karo, karo, 256), dtype=np.float32)
    for i in range(karo):
        for j in range(karo):
            parca = genis[i * kh:(i + 1) * kh, j * kw:(j + 1) * kw]
            hist = np.bincount(parca.ravel(), minlength=256)

            fazla = np.maximum(0, hist - limit).sum()
            hist = np.minimum(hist, limit)
            dagitilacak = fazla // 256
            kalan = fazla % 256
            hist += dagitilacak
            hist[:kalan] += 1

            cdf = hist.cumsum()
            cdf_min = cdf[cdf > 0].min()
            denom = cdf[-1] - cdf_min
            if denom == 0:
                tablolar[i, j] = np.arange(256, dtype=np.float32)
            else:
                tablolar[i, j] = np.clip((cdf - cdf_min) * 255.0 / denom, 0, 255)

    # 2. Çift doğrusal enterpolasyon (Bilinear interpolation)
    sonuc = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        ty = (y + 0.5) / kh - 0.5
        i0 = int(np.floor(ty))
        i1 = i0 + 1
        ay = ty - i0
        i0 = max(0, min(karo - 1, i0))
        i1 = max(0, min(karo - 1, i1))

        for x in range(w):
            tx = (x + 0.5) / kw - 0.5
            j0 = int(np.floor(tx))
            j1 = j0 + 1
            ax = tx - j0
            j0 = max(0, min(karo - 1, j0))
            j1 = max(0, min(karo - 1, j1))

            val = gri[y, x]
            v00 = tablolar[i0, j0, val]
            v01 = tablolar[i0, j1, val]
            v10 = tablolar[i1, j0, val]
            v11 = tablolar[i1, j1, val]

            top = (1 - ax) * v00 + ax * v01
            bot = (1 - ax) * v10 + ax * v11
            pix = (1 - ay) * top + ay * bot
            sonuc[y, x] = int(round(pix))

    return sonuc


def main():
    CIKTI_KLASOR.mkdir(parents=True, exist_ok=True)
    clahe_cv = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    rapor_satirlari = ["Ödev 3.3: CLAHE Karşılaştırma Raporu", "-" * 60]

    for ad in ["dag", "sis"]:
        girdi_yolu = GIRDI_KLASOR / f"{ad}.jpg"
        gri = cv2.imread(str(girdi_yolu), cv2.IMREAD_GRAYSCALE)
        if gri is None:
            continue

        cv_sonuc = clahe_cv.apply(gri)
        ozel_sonuc = clahe_ozel(gri, clip_limit=2.0, karo=8)

        fark = np.abs(cv_sonuc.astype(int) - ozel_sonuc.astype(int))
        maks_fark = int(fark.max())
        farkli_piksel_orani = (np.count_nonzero(fark > 0) / gri.size) * 100.0

        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_opencv.png"), cv_sonuc)
        cv2.imwrite(str(CIKTI_KLASOR / f"{ad}_ozel.png"), ozel_sonuc)

        bilgi = (
            f"Görsel: {ad}.jpg\n"
            f"  * Orijinal Standart Sapma : {gri.std():.2f}\n"
            f"  * CLAHE Standart Sapma    : {cv_sonuc.std():.2f}\n"
            f"  * OpenCV vs. Özel Maksimum Fark: {maks_fark} (Farklı piksel oranı: %{farkli_piksel_orani:.2f} - float enterpolasyon yuvarlaması)\n"
        )
        print(bilgi)
        rapor_satirlari.append(bilgi)

    with open(CIKTI_KLASOR / "rapor.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))


if __name__ == "__main__":
    main()
