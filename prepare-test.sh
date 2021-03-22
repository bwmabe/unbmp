#!/usr/bin/env bash

rm -r test/test_dir
rm -r test/test_files

mkdir test/test_dir
mkdir test/test_files

cp test/test_images/* test/test_dir/
cp test/test_images/* test/test_files/

# Globbing should work?
echo ""
echo "./unbmp png test/test_files/*"
echo "--------------------------------"
./unbmp png test/test_files/*

echo ""
echo "./unbmp png -d test/test_dir -s bmp"
echo "--------------------------------"
./unbmp png -d test/test_dir -s bmp

echo ""
echo "./unbmp jpg -d test/test_dir -s png"
echo "--------------------------------"
./unbmp jpg -d test/test_dir -s png
