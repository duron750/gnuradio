sudo pkg install py311-numpy py311-pygccxml py311-pybind11 pybind11 py311-mako mako py311-pyyaml qt5 py311-thrift py311-jsonschema doxygen py311-cheetah3 fftw3 fftw spdlog py311-pyqtgraph py311-lxml qwtplot3d-qt5 qwt6-qt5
sudo pkg install SoapyAirspy SoapyHackRF SoapySDR py311-SoapySDR airspy hackrf-2024
git clone --recursive https://github.com/gnuradio/volk
cd volk
mkdir build
cd build
cmake ../
make
sudo make install
volk_profile
cd ../../
git clone https://github.com/gnuradio/gnuradio
sed -i '' 's/pthread_set_name_np/pthread_setname_np/g' gnuradio/gnuradio-runtime/lib/thread/thread.cc
cd gnuradio
mkdir buid
cd build
cmake -DENABLE_GR_ANALOG=ON -DENABLE_GR_FILTER=ON -DENABLE_GR_FFT=ON -DENABLE_GR_BLOCKS=ON -DENABLE_GRC=ON -DENABLE_GR_DIGITAL=ON -DENABLE_GNURADIO_RUNTIME=ON -DENABLE_GR_QTGUI=ON -DQWT_INCLUDE_DIRS=/usr/local/include/qt5/qwt6 -DQWT_LIBRARIES=/usr/local/lib/qt5/libqwt.so -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/local/bin/python3 ../
make -j 4
sudo make install
cd ../../
git clone https://github.com/bastibl/gr-rds
cd gr-rds
mkdir build
cd build
cmake ../
make -j 4
sudo make install


