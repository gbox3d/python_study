# intel real sense camera

## ubuntu 

```bash
pip install pyrealsense2
```

## windows

```bash
pip install pyrealsense2
```

## udev 설정

이 설정을 안하면 보안상의 문재로 항상 로컬머신이 로그인상태일때만 원격으로 사용가능하다(원격 사용시 불편함)

```bash
cd ~
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/ 

sudo su
udevadm control --reload-rules && udevadm trigger
exit

```

## pi 4

### 바이너리 설치  
```bash
sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils
```

### 직접 빌드하여설치 하기  
작업은 rasbian64 lite 에서 테스트했으며 문제 없이 동작함을 확인함.(2023.6.29 현제)    

빌드를 위해서 swap 파일 늘리기

```bash
sudo vim /etc/dphys-swapfile

# Increase swap to 2GB by changing the file below to CONF_SWAPSIZE=2048:

sudo /etc/init.d/dphys-swapfile restart swapon -s #Apply the change:
```

필수 모듈 설치

```bash

sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install automake libtool vim cmake libusb-1.0-0-dev libx11-dev xorg-dev libglu1-mesa-dev
sudo apt-get install libssl-dev
sudo apt-get install pip
export OPENSSL_ROOT_DIR=/usr/include/openssl
```

udev rule 추가

```bash
cd ~
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/ 

sudo su
udevadm control --reload-rules && udevadm trigger
exit

```

빌드

```bash
echo "export LD_LIBRARY_PATH=/usr/local/lib:\$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc

# protobuf 빌드
cd ~
git clone --depth=1 -b v3.10.0 https://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j1
sudo make install
cd python
export LD_LIBRARY_PATH=../src/.libs
python3 setup.py build --cpp_implementation 
python3 setup.py test --cpp_implementation
sudo python3 setup.py install --cpp_implementation
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3
sudo ldconfig
protoc --version

# libtbb-dev 빌드(c++ thread 라이브러리)
cd ~
wget https://github.com/PINTO0309/TBBonARMv7/raw/master/libtbb-dev_2018U2_armhf.deb
sudo dpkg -i ~/libtbb-dev_2018U2_armhf.deb
sudo ldconfig
rm libtbb-dev_2018U2_armhf.deb

# librealsense 빌드
cd ~/librealsense
mkdir  build  && cd build
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release -DFORCE_LIBUVC=true
make -j1
sudo make install

# python wrapper 빌드
cd ~/librealsense/build
cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)
make -j1
sudo make install

# python path 설정
echo 'export PYTHONPATH=$PYTHONPATH:~/librealsense/build/wrappers/python' >> ~/.bashrc
source ~/.bashrc
```

## ref
[공식문서 바로가기](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python)  
[파이썬 예제](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples)
[pi4]( https://github.com/datasith/Ai_Demos_RPi/wiki/Raspberry-Pi-4-and-Intel-RealSense-D435)
