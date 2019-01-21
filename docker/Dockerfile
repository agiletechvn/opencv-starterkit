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

ARG FAST_BUILD

RUN if [ "FAST_BUILD" = "true" ] ; then

# easiest way
# mkdir build
# cd build
# cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON -DENABLE_PRECOMPILED_HEADERS=OFF ..
# make -j4 && make install && ldconfig
# rm -rf OpenCV
# if have 8 cores then make -j8
# Dbus problem: apt-get install -y dbus-x11



wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
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
&& make install && ldconfig \
&& rm /${OPENCV_VERSION}.zip \
&& rm -rf /opencv-${OPENCV_VERSION} \
&& ln -s \
  /usr/python/cv2/python-${PYTHON_VERSION}/cv2.cpython-*.so \
  /usr/local/lib/python${PYTHON_VERSION}/dist-packages/cv2.so

else 

apt -y install libgtk2.0-dev libtbb-dev qt5-default \
&& git clone https://github.com/opencv/opencv.git \
&& cd opencv \
&& git checkout $OPENCV_VERSION \
&& cd .. \
 
&& git clone https://github.com/opencv/opencv_contrib.git \
&& cd opencv_contrib \
&& git checkout $OPENCV_VERSION \
&& cd .. \
&& cd opencv && mkdir build && cd build \
&& cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D INSTALL_C_EXAMPLES=OFF \
  -D INSTALL_PYTHON_EXAMPLES=OFF \
  -D WITH_TBB=ON \
  -D WITH_V4L=ON \
  -D OPENCV_PYTHON3_INSTALL_PATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages/ \
  -D WITH_QT=ON \
  -D WITH_OPENGL=ON \
  -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
  -D BUILD_EXAMPLES=ON .. \
&& make -j4 \
&& make install \
&& rm -rf opencv \
&& rm -rf opencv_contrib 

fi

# Done

