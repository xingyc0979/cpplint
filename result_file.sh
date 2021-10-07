#!/bin/bash
#hnh
mkdir -p cpplint
mkdir -p /home/test
sed -i '/^Total/a\\n' ./cpplint.txt
cp ./cpplint.txt ./cpplint/
zip -r cpplint_details.zip ./cpplint
cp ./cpplint_details.zip /home/test/
