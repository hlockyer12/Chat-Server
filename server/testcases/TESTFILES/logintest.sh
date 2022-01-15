#!/bin/bash

coverage run ../server.py 2050 &
sleep 1

python3 ../client.py 2050 INPUT/logintest_client1.in > ./OUTPUT/logintest_client1.out &
sleep 2

python3 ../client.py 2050 INPUT/logintest_client2.in > ./OUTPUT/logintest_client2.out &
sleep 2

DIFF1=$(diff -q ./OUTPUT/logintest_client1.out ./EXPECTED/logintest_client1.exp)
DIFF2=$(diff -q ./OUTPUT/logintest_client2.out ./EXPECTED/logintest_client2.exp)

if [ "$DIFF1" == "" ]
then
    contents1=$(jq '.LoginTests.logintest_client1 |= "Passed"' testing.json) && \
    echo "${contents1}" > testing.json
fi

if [ "$DIFF2" == "" ]
then
    contents2=$(jq '.LoginTests.logintest_client2 |= "Passed"' testing.json) && \
    echo "${contents2}" > testing.json
fi

if [ "$DIFF1" == "" ] && [ "$DIFF2" == "" ]
then
    echo PASSED
else
    echo FAILED
fi


echo Login tests complete!
echo