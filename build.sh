# alternative option if not using CMake
# mkdir build && cd build && cmake .. && cd ..
# cmake --build build/ --config Release

# echo $1
BASE_DIR=$PWD
OUTPUT=""
# # remove extension
while [ "$#" -gt 0 ]; do
  INPUT=${1%%.*}  
  OUTPUT="$OUTPUT\nadd_example($INPUT)"
  shift 
done
PROJECT=`basename $BASE_DIR`
# # build
# echo 'g++ -std=c++0x `pkg-config --cflags opencv` '$INPUT' `pkg-config --libs opencv` -o '$OUTPUT
# g++ -std=c++0x `pkg-config --cflags opencv` $INPUT `pkg-config --libs opencv` -o $OUTPUT


makelists=$(cat <<EOF
cmake_minimum_required(VERSION 3.1)
# Enable C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY \${CMAKE_BINARY_DIR}/..)
SET(OpenCV_DIR /usr/lib/x86_64-linux-gnu/cmake/opencv4)

PROJECT($PROJECT)

find_package( OpenCV REQUIRED )

include_directories( \${OpenCV_INCLUDE_DIRS})

MACRO(add_example name)
  ADD_EXECUTABLE(\${name} \${name}.cpp)
  TARGET_LINK_LIBRARIES(\${name} \${OpenCV_LIBS})
ENDMACRO()

$OUTPUT
EOF
)

if [ -d build ] && [ -f CMakeLists.txt ];then
  echo "Build ..."
  cmake --build build/ --config Release  
else
  echo "Create CMakeLists.txt and build ..."
  echo -e "$makelists" > CMakeLists.txt
  mkdir -p build && cd build && cmake .. && cd ..
  cmake --build build/ --config Release
fi