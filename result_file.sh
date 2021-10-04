#!/bin/bash
#hnh
mkdir -p cpplint
mkdir -p /home/test
sed -i '/^Total/a\\n' ./cpplint.txt
cp ./cpplint.txt ./cpplint/
zip -r cpplint_details.zip ./cpplint
cp ./cpplint_details.zip /home/test/
sed -i "/Ignor/d" ./cpplint.txt
sed -i "/Done/d" ./cpplint.txt
head -n 10 ./cpplint.txt > tmp.txt
cat tmp.txt > cpplint.txt
sed -i "s/\/home\/test\///" ./cpplint.txt
sed -i 's/:/#/g' ./cpplint.txt
sed -i 's/)/):/' ./cpplint.txt
sed -i 's/"//g' ./cpplint.txt
sed -i 's/cpplint/&:/' ./cpplint.txt
sed -i 's/(/:&/' ./cpplint.txt
sed -i 's/]/&:/' ./cpplint.txt
sed -i "s/\[/:&/2" ./cpplint.txt
echo -e '{\n"error":[' >tmp.txt
awk 'BEGIN{FS=":"}{print "{ ""\"""file_name""\""":""\""$1"\""", ""\"""start""\""":""\""$2"\""", ""\"""type""\""":""\""$4"\""", ""\"""desc""\""":""\""$5"\""",""\"""level""\""":""\""$6"\""" },"}' ./cpplint.txt >> tmp.txt
sed -i '$s/.$//' ./tmp.txt
echo -e ']\n}' >> tmp.txt
sed -i 's/"#/"/' ./tmp.txt
sed -i 's/" #/"/' ./tmp.txt
cat tmp.txt > cpplint.txt
sed -i 's/(//' ./cpplint.txt
sed -i 's/)//' ./cpplint.txt
cp ./cpplint.txt /home/test/cpplint_overviews.json
