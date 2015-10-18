#!/bin/bash
wget https://raw.githubusercontent.com/ssdoz2sk/NCYU/master/HW/Setup.dist
wget http://python.org/ftp/python/3.4.0/Python-3.4.0.tar.xz
tar -xf Python-3.4.0.tar.xz
mv -f ./Setup.dist ./Python-3.4.0/Modules/Setup.dist
cd Python-3.4.0
./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make 
make altinstall
