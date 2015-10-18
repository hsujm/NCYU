#!/bin/bash

wget http://python.org/ftp/python/3.4.0/Python-3.4.0.tar.xz
tar xf Python-3.4.0.tar.xz
cd Python-3.4.0
./configure --prefix=/usr/local --enable-shared
make 
make altinstall
