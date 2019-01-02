# using python 3
# need https://github.com/NVIDIA/nvidia-docker 
# FROM tensorflow/tensorflow:latest-gpu-py3
FROM tensorflow/tensorflow:latest-py3
MAINTAINER Thanh Tu <tu@agiletech.vn>

RUN apt-get update \
&& apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy scipy click pandas matplotlib seaborn tensorflow-hub

# install tesseract 4
RUN add-apt-repository ppa:alex-p/tesseract-ocr \
&& apt-get update \
&& apt install -y tesseract-ocr libtesseract-dev \
&& pip install pytesseract

WORKDIR /

ENV PYTHON_VERSION="3.5"
ENV OPENCV_VERSION="4.0.0"

RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
&& unzip ${OPENCV_VERSION}.zip \
&& mkdir /opencv-${OPENCV_VERSION}/cmake_binary \
&& cd /opencv-${OPENCV_VERSION}/cmake_binary \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DCMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python) \
  -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
  .. \
&& make install 

# make sure site-packages existed
RUN ln -s \
  /usr/python/cv2/python-${PYTHON_VERSION}/cv2.cpython-*.so \
  /usr/local/lib/python${PYTHON_VERSION}/dist-packages/cv2.so

RUN rm /${OPENCV_VERSION}.zip \
    && rm -r /opencv-${OPENCV_VERSION} 
