INPUT=$1
# remove extension
OUTPUT=${INPUT%%.*}
# build
echo 'g++ -std=c++0x `pkg-config --cflags opencv` '$INPUT' `pkg-config --libs opencv` -o '$OUTPUT
g++ -std=c++0x `pkg-config --cflags opencv` $INPUT `pkg-config --libs opencv` -o $OUTPUT