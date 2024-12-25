#!/bin/bash

mkdir tmp

magick inputs/test1.jpg -modulate 100,300 tmp/test1_alt.jpg

magick tmp/test1_alt.jpg -quality 5 outputs/test1_damaged.jpg

rm ./tmp/*

rmdir tmp