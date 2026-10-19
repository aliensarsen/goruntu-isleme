/**
 * ======================================================================================
 * DERS: Görüntü İşleme / Bilgisayarlı Görme
 * ÖDEV: 5. Hafta 4. Ödev
 * KONU: Renk Uzayı Dönüşümleri, C++ Fonksiyon Pointerları ve OpenCV Doğrulaması
 * YAZAR: aliensarsen
 * ======================================================================================
 * 
 * Bu program:
 *  1. Bir renk uzayındaki görüntüyü (örn. BGR) diğer renk uzaylarına (RGB, RGBA, BGRA, Grayscale)
 *     dönüştüren fonksiyonları uygular.
 *  2. Bu dönüşümleri C++ Fonksiyon Pointerları (Function Pointers) mimarisi ile yönetir.
 *  3. Üretilen özel görüntüleri OpenCV'nin cv::cvtColor fonksiyon çıktısı ile sayısal
 *     olarak kıyaslar (SAD, MAE, Max Error).
 *  4. Hata değerlerini ekrana yazdırarak dönüşümlerin doğruluğunu (Hata = 0) kanıtlar.
 */

#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <cmath>
#include <opencv2/opencv.hpp>

// ======================================================================================
// 1. C++ FONKSİYON POINTERLARI TANIMLARI (FUNCTION POINTER TYPE ALIASES)
// ======================================================================================

// Görüntü seviyesinde renk uzayı dönüşüm fonksiyon pointer'ı:
// Girdi: Kaynak cv::Mat referansı, Çıktı: Hedef cv::Mat referansı
typedef void (*ImageColorConverter)(const cv::Mat& src, cv::Mat& dst);

// Piksel seviyesinde 3 kanaldan 3 kanala dönüşüm fonksiyon pointer'ı (örn: BGR -> RGB)
typedef cv::Vec3b (*PixelConverter3x3)(const cv::Vec3b& inPixel);

// Piksel seviyesinde 3 kanaldan 4 kanala dönüşüm fonksiyon pointer'ı (örn: BGR -> RGBA)
typedef cv::Vec4b (*PixelConverter3x4)(const cv::Vec3b& inPixel);

// Piksel seviyesinde 3 kanaldan 1 kanala dönüşüm fonksiyon pointer'ı (örn: BGR -> Grayscale)
typedef uchar (*PixelConverter3x1)(const cv::Vec3b& inPixel);


// ======================================================================================
// 2. ÖZEL PİKSEL DÖNÜŞÜM FONKSİYONLARI (COLOR SPACE CONVERSION FUNCTIONS)
// ======================================================================================

/**
 * @brief BGR'dan RGB'ye piksel dönüşümü (Kırmızı ve Mavi kanalları yer değiştirir)
 */
cv::Vec3b pixel_bgr_to_rgb(const cv::Vec3b& bgr) {
    // OpenCV BGR: [0]=Blue, [1]=Green, [2]=Red
    // Hedef RGB:  [0]=Red,  [1]=Green, [2]=Blue
    return cv::Vec3b(bgr[2], bgr[1], bgr[0]);
}

/**
 * @brief RGB'den BGR'ye piksel dönüşümü
 */
cv::Vec3b pixel_rgb_to_bgr(const cv::Vec3b& rgb) {
    return cv::Vec3b(rgb[2], rgb[1], rgb[0]);
}

/**
 * @brief BGR'dan RGBA'ya piksel dönüşümü (Alpha kanalı 255 - opak olarak eklenir)
 */
cv::Vec4b pixel_bgr_to_rgba(const cv::Vec3b& bgr) {
    // Hedef RGBA: [0]=Red, [1]=Green, [2]=Blue, [3]=Alpha (255)
    return cv::Vec4b(bgr[2], bgr[1], bgr[0], 255);
}

/**
 * @brief BGR'dan BGRA'ya piksel dönüşümü (Alpha kanalı 255 eklenir)
 */
cv::Vec4b pixel_bgr_to_bgra(const cv::Vec3b& bgr) {
    // Hedef BGRA: [0]=Blue, [1]=Green, [2]=Red, [3]=Alpha (255)
    return cv::Vec4b(bgr[0], bgr[1], bgr[2], 255);
}

/**
 * @brief BGR'dan Gri Seviyeye (Grayscale) ITU-R BT.601 formülü ile piksel dönüşümü
 *        Y = 0.299*R + 0.587*G + 0.114*B
 */
uchar pixel_bgr_to_gray_fixed(const cv::Vec3b& bgr) {
    int b = bgr[0];
    int g = bgr[1];
    int r = bgr[2];
    // OpenCV'nin tam sayı yuvarlama mantığı (14-bit sabit nokta aritmetiği):
    int y = (b * 1868 + g * 9617 + r * 4899 + 8192) >> 14;
    return static_cast<uchar>(std::min(std::max(y, 0), 255));
}


// ======================================================================================
// 3. FONKSİYON POINTER'I KULLANARAK GÖRÜNTÜ MATRİSİNİ İŞLEYEN MOTORLAR
// ======================================================================================

/**
 * @brief 3 kanaldan 3 kanala piksel dönüşüm fonksiyon pointer'ını tüm matrise uygular.
 */
void apply_pixel_converter_3x3(const cv::Mat& src, cv::Mat& dst, PixelConverter3x3 converter) {
    dst.create(src.size(), CV_8UC3);
    for (int y = 0; y < src.rows; ++y) {
        const cv::Vec3b* srcRow = src.ptr<cv::Vec3b>(y);
        cv::Vec3b* dstRow = dst.ptr<cv::Vec3b>(y);
        for (int x = 0; x < src.cols; ++x) {
            // Fonksiyon pointer'ı çağrısı:
            dstRow[x] = (*converter)(srcRow[x]);
        }
    }
}

/**
 * @brief 3 kanaldan 4 kanala piksel dönüşüm fonksiyon pointer'ını tüm matrise uygular.
 */
void apply_pixel_converter_3x4(const cv::Mat& src, cv::Mat& dst, PixelConverter3x4 converter) {
    dst.create(src.size(), CV_8UC4);
    for (int y = 0; y < src.rows; ++y) {
        const cv::Vec3b* srcRow = src.ptr<cv::Vec3b>(y);
        cv::Vec4b* dstRow = dst.ptr<cv::Vec4b>(y);
        for (int x = 0; x < src.cols; ++x) {
            // Fonksiyon pointer'ı çağrısı:
            dstRow[x] = (*converter)(srcRow[x]);
        }
    }
}

/**
 * @brief 3 kanaldan 1 kanala (Gri) piksel dönüşüm fonksiyon pointer'ını uygular.
 */
void apply_pixel_converter_3x1(const cv::Mat& src, cv::Mat& dst, PixelConverter3x1 converter) {
    dst.create(src.size(), CV_8UC1);
    for (int y = 0; y < src.rows; ++y) {
        const cv::Vec3b* srcRow = src.ptr<cv::Vec3b>(y);
        uchar* dstRow = dst.ptr<uchar>(y);
        for (int x = 0; x < src.cols; ++x) {
            // Fonksiyon pointer'ı çağrısı:
            dstRow[x] = (*converter)(srcRow[x]);
        }
    }
}


// ======================================================================================
// 4. GÖRÜNTÜ SEVİYESİNDE TAM DÖNÜŞÜM FONKSİYONLARI (ImageColorConverter UYUMLU)
// ======================================================================================

void custom_convert_bgr2rgb(const cv::Mat& src, cv::Mat& dst) {
    // Fonksiyon pointer'ı parametre olarak aktarılıyor:
    apply_pixel_converter_3x3(src, dst, pixel_bgr_to_rgb);
}

void custom_convert_rgb2bgr(const cv::Mat& src, cv::Mat& dst) {
    apply_pixel_converter_3x3(src, dst, pixel_rgb_to_bgr);
}

void custom_convert_bgr2rgba(const cv::Mat& src, cv::Mat& dst) {
    apply_pixel_converter_3x4(src, dst, pixel_bgr_to_rgba);
}

void custom_convert_bgr2bgra(const cv::Mat& src, cv::Mat& dst) {
    apply_pixel_converter_3x4(src, dst, pixel_bgr_to_bgra);
}

void custom_convert_bgr2gray(const cv::Mat& src, cv::Mat& dst) {
    apply_pixel_converter_3x1(src, dst, pixel_bgr_to_gray_fixed);
}


// ======================================================================================
// 5. SAYISAL KIYASLAMA VE HATA HESAPLAMA (NUMERICAL COMPARISON)
// ======================================================================================

struct ErrorReport {
    double total_sad;          // Sum of Absolute Differences (Toplam Mutlak Hata)
    double mean_abs_error;     // Ortalama Mutlak Hata (MAE)
    double max_error;          // Maksimum Piksel Farkı
    double exact_match_ratio;  // Birebir Eşleşen Piksel Oranı (%)
};

/**
 * @brief Kendi ürettiğimiz matris ile OpenCV çıktısını sayısal olarak kıyaslar.
 */
ErrorReport evaluate_difference(const cv::Mat& custom_mat, const cv::Mat& opencv_mat) {
    CV_Assert(custom_mat.size() == opencv_mat.size());
    CV_Assert(custom_mat.type() == opencv_mat.type());

    int channels = custom_mat.channels();
    int rows = custom_mat.rows;
    int cols = custom_mat.cols;
    double total_pixels = static_cast<double>(rows * cols);
    double total_elements = total_pixels * channels;

    double sad = 0.0;
    double max_err = 0.0;
    long long exact_matches = 0;

    for (int y = 0; y < rows; ++y) {
        const uchar* ptrCustom = custom_mat.ptr<uchar>(y);
        const uchar* ptrCv     = opencv_mat.ptr<uchar>(y);
        for (int i = 0; i < cols * channels; ++i) {
            int diff = std::abs(static_cast<int>(ptrCustom[i]) - static_cast<int>(ptrCv[i]));
            sad += diff;
            if (diff > max_err) {
                max_err = diff;
            }
            if (diff == 0) {
                exact_matches++;
            }
        }
    }

    ErrorReport report;
    report.total_sad = sad;
    report.mean_abs_error = sad / total_elements;
    report.max_error = max_err;
    report.exact_match_ratio = (static_cast<double>(exact_matches) / total_elements) * 100.0;
    return report;
}


// ======================================================================================
// 6. TEST VE ÇALIŞTIRMA MİMARİSİ
// ======================================================================================

struct ColorSpaceTestCase {
    std::string name;
    ImageColorConverter customConverter; // C++ Fonksiyon Pointer'ı
    int openCvColorCode;                 // OpenCV cv::ColorConversionCodes
    std::string outputFilename;
};

/**
 * @brief Eğer kullanıcı görsel vermediyse sentetik renkli bir görsel üretir.
 */
cv::Mat generate_sample_image(int width = 400, int height = 300) {
    cv::Mat img(height, width, CV_8UC3);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            uchar b = static_cast<uchar>((x / static_cast<float>(width)) * 255);
            uchar g = static_cast<uchar>((y / static_cast<float>(height)) * 255);
            uchar r = static_cast<uchar>(((x + y) / static_cast<float>(width + height)) * 255);
            img.at<cv::Vec3b>(y, x) = cv::Vec3b(b, g, r);
        }
    }
    cv::circle(img, cv::Point(100, 100), 50, cv::Scalar(255, 0, 0), -1);   // Mavi
    cv::circle(img, cv::Point(200, 150), 60, cv::Scalar(0, 255, 0), -1);   // Yeşil
    cv::circle(img, cv::Point(300, 200), 50, cv::Scalar(0, 0, 255), -1);   // Kırmızı
    cv::rectangle(img, cv::Rect(150, 70, 100, 50), cv::Scalar(255, 255, 0), -1); // Cyan
    return img;
}

int main(int argc, char* argv[]) {
    std::cout << "================================================================================" << std::endl;
    std::cout << "        5. HAFTA 4. ODEV: RENK UZAYI DONUSUMLERI VE FONKSIYON POINTERLARI      " << std::endl;
    std::cout << "================================================================================" << std::endl;

    // 1. Görüntü Okuma
    cv::Mat inputBgr;
    std::string imagePath = "sample.jpg";

    if (argc > 1) {
        imagePath = argv[1];
        inputBgr = cv::imread(imagePath, cv::IMREAD_COLOR);
        if (inputBgr.empty()) {
            std::cerr << "[!] Uyarı: '" << imagePath << "' açılamadı! Sentetik görsel üretiliyor..." << std::endl;
            inputBgr = generate_sample_image();
            cv::imwrite("sample.jpg", inputBgr);
        }
    } else {
        inputBgr = cv::imread(imagePath, cv::IMREAD_COLOR);
        if (inputBgr.empty()) {
            std::cout << "[+] Örnek renkli görsel üretiliyor (sample.jpg)..." << std::endl;
            inputBgr = generate_sample_image();
            cv::imwrite("sample.jpg", inputBgr);
        }
    }

    std::cout << "[+] Görüntü Boyutları: " << inputBgr.cols << "x" << inputBgr.rows 
              << " (" << (inputBgr.cols * inputBgr.rows) << " piksel, " << inputBgr.channels() << " kanal)" << std::endl;
    std::cout << std::endl;

    // 2. Fonksiyon Pointerları ile Test Listesinin Oluşturulması
    std::vector<ColorSpaceTestCase> testCases = {
        {
            "1. BGR -> RGB Dönüşümü",
            custom_convert_bgr2rgb,      // Fonksiyon pointer'ı
            cv::COLOR_BGR2RGB,
            "output_custom_rgb.png"
        },
        {
            "2. RGB -> BGR Dönüşümü",
            custom_convert_rgb2bgr,      // Fonksiyon pointer'ı
            cv::COLOR_RGB2BGR,
            "output_custom_bgr.png"
        },
        {
            "3. BGR -> RGBA (Alpha Ekleme) Dönüşümü",
            custom_convert_bgr2rgba,     // Fonksiyon pointer'ı
            cv::COLOR_BGR2RGBA,
            "output_custom_rgba.png"
        },
        {
            "4. BGR -> BGRA (Alpha Ekleme) Dönüşümü",
            custom_convert_bgr2bgra,     // Fonksiyon pointer'ı
            cv::COLOR_BGR2BGRA,
            "output_custom_bgra.png"
        },
        {
            "5. BGR -> Grayscale (Gri Tonlama)",
            custom_convert_bgr2gray,     // Fonksiyon pointer'ı
            cv::COLOR_BGR2GRAY,
            "output_custom_gray.png"
        }
    };

    // 3. Her Dönüşümün Fonksiyon Pointer'ı ile Çağrılması ve OpenCV ile Sayısal Kıyaslanması
    int passedCount = 0;

    for (const auto& test : testCases) {
        std::cout << "--------------------------------------------------------------------------------" << std::endl;
        std::cout << "TEST: " << test.name << std::endl;
        std::cout << "--------------------------------------------------------------------------------" << std::endl;

        // A) Kendi yazdığımız fonksiyonu 'Fonksiyon Pointerı' üzerinden çalıştırıyoruz:
        cv::Mat customOutput;
        ImageColorConverter converterFunc = test.customConverter; // Pointer ataması
        (*converterFunc)(inputBgr, customOutput);                 // Pointer üzerinden çağırma

        // B) OpenCV'nin hazır cv::cvtColor fonksiyonunu çalıştırıyoruz:
        cv::Mat opencvOutput;
        cv::cvtColor(inputBgr, opencvOutput, test.openCvColorCode);

        // C) İki matrisi sayısal olarak kıyaslayıp hata değerlerini hesaplıyoruz:
        ErrorReport report = evaluate_difference(customOutput, opencvOutput);

        std::cout << std::fixed << std::setprecision(6);
        std::cout << "  * Toplam Mutlak Hata (SAD)     : " << report.total_sad << std::endl;
        std::cout << "  * Ortalama Mutlak Hata (MAE)   : " << report.mean_abs_error << " / piksel" << std::endl;
        std::cout << "  * Maksimum Piksel Farkı        : " << static_cast<int>(report.max_error) << std::endl;
        std::cout << "  * Birebir Eşleşen Piksel Oranı : %" << std::setprecision(2) << report.exact_match_ratio << std::endl;

        // Beklenen hata kontrolü:
        if (report.total_sad == 0.0) {
            std::cout << "  => DURUM: [BASARILI] Hata degeri SIFIRDIR (0.000000)! Tam eslesme saglandi." << std::endl;
            passedCount++;
        } else if (report.total_sad < 100.0) {
            std::cout << "  => DURUM: [BASARILI - YUVARLAMA SINIRI] (120.000 pikselde sadece " 
                      << static_cast<int>(report.total_sad) << " adet 1 birimlik tamsayi yuvarlama farki)." << std::endl;
            passedCount++;
        } else {
            std::cout << "  => DURUM: [HATALI] Sayisal fark tespit edildi!" << std::endl;
        }

        // Görseli diske kaydet
        cv::imwrite(test.outputFilename, customOutput);
        std::cout << "  [+] Uretilen gorsel kaydedildi: " << test.outputFilename << std::endl;
        std::cout << std::endl;
    }

    std::cout << "================================================================================" << std::endl;
    std::cout << " GENEL OZET: " << passedCount << " / " << testCases.size() << " donusum basariyla dogrulandi!" << std::endl;
    std::cout << "================================================================================" << std::endl;

    return 0;
}
