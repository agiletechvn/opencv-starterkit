# alternative option if not using CMake
# mkdir build && cd build && cmake .. && cd ..
# cmake --build build/ --config Release

# echo $1
BASE_DIR=$PWD
ARGS=()
CMAKE_FILE=CMakeLists.txt
# # remove extension
while [ "$#" -gt 0 ]; do
  INPUT=${1%%.*}    
  ARGS+=("add_example($INPUT)")
  shift 
done
PROJECT=`basename $BASE_DIR`
# # build
# echo 'g++ -std=c++0x `pkg-config --cflags opencv` '$INPUT' `pkg-config --libs opencv` -o '$OUTPUT
# g++ -std=c++0x `pkg-config --cflags opencv` $INPUT `pkg-config --libs opencv` -o $OUTPUT

saveMakeLists(){  
  local str=$(cat <<EOF
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

$1
EOF
  )

  echo -e "$str" > $CMAKE_FILE
}

if [ -d build ] && [ -f CMakeLists.txt ];then  
  # check if not exsisted then append  
  for ARG in "${ARGS[@]}";do
    if ! grep -q $ARG "$CMAKE_FILE"; then
      echo "Add target $ARG"
      echo "$ARG" >> $CMAKE_FILE
    fi
  done   
else
  echo "Create $CMAKE_FILE and build ..."
  OUTPUT=$(IFS=$'\n'; echo "${ARGS[*]}")
  saveMakeLists "$OUTPUT"
  mkdir -p build && cd build && cmake .. && cd ..  
fi

echo "Building ..."
cmake --build build/ --config Release