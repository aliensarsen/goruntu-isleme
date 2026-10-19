# 5. Hafta 4. Ödev Makefile

CXX = clang++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra

# OpenCV Include ve Kütüphane Yolları (Homebrew / macOS)
OPENCV_PREFIX ?= /opt/homebrew/opt/opencv
INCLUDES = -I$(OPENCV_PREFIX)/include/opencv5
LDFLAGS = -L$(OPENCV_PREFIX)/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui

TARGET = color_convert
SRCS = main.cpp

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SRCS) -o $(TARGET) $(LDFLAGS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) output_*.png sample.jpg
