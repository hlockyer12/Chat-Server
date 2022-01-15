#!/bin/bash

coverage run ../server.py 2090 &
sleep 1

python3 ../client.py 2090 INPUT/saytest_client1.in > ./OUTPUT/saytest_client1.out &
sleep 2

python3 ../client.py 2090 INPUT/saytest_client2.in > ./OUTPUT/saytest_client2.out &
sleep 2

python3 ../client.py 2090 INPUT/saytest_client3.in > ./OUTPUT/saytest_client3.out &
sleep 2

DIFF1=$(diff -q ./OUTPUT/saytest_client1.out ./EXPECTED/saytest_client1.exp)
DIFF2=$(diff -q ./OUTPUT/saytest_client2.out ./EXPECTED/saytest_client2.exp)
DIFF3=$(diff -q ./OUTPUT/saytest_client3.out ./EXPECTED/saytest_client3.exp)

if [ "$DIFF1" == "" ]
then
    contents1=$(jq '.SayTests.saytest_client1 |= "Passed"' testing.json) && \
    echo "${contents1}" > testing.json
fi

if [ "$DIFF2" == "" ]
then
    contents2=$(jq '.SayTests.saytest_client2 |= "Passed"' testing.json) && \
    echo "${contents2}" > testing.json
fi

if [ "$DIFF3" == "" ]
then
    contents3=$(jq '.SayTests.saytest_client3 |= "Passed"' testing.json) && \
    echo "${contents3}" > testing.json
fi

if [ "$DIFF1" == "" ] && [ "$DIFF2" == "" ] && [ "$DIFF3" == "" ]
then
    echo PASSED
else
    echo FAILED
fi

echo Say tests complete!
echo