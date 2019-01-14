## Compile the code

```bash
apt install libopencv-dev libopencv-calib3d-dev -y
g++ -std=c++0x `pkg-config --cflags opencv` hello-world.cpp `pkg-config --libs opencv` -o helloworld
```

## Run X11 UI from docker container on MacOSX

```bash
brew install socat
brew cask install xquartz
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"
open -a XQuarts
MACOSX_IP=`ifconfig en0 inet | grep inet | awk '{print $2}'`
# in docker container:
export DISPLAY=<MACOSX_IP>:0
```

Currently libopencv-dev is opencv3

Please see the following [blog post](https://www.learnopencv.com/cvui-gui-lib-built-on-top-of-opencv-drawing-primitives/) for more details about this code

[cvui: A GUI lib built on top of OpenCV drawing primitives](https://www.learnopencv.com/cvui-gui-lib-built-on-top-of-opencv-drawing-primitives/)
