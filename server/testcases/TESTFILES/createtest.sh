#!/bin/bash

coverage run ../server.py 2060 &
serverid=$!
sleep 1

python3 ../client.py 2060 INPUT/createtest_client1.in > ./OUTPUT/createtest_client1.out &
sleep 2

python3 ../client.py 2060 INPUT/createtest_client2.in > ./OUTPUT/createtest_client2.out &
sleep 2

DIFF1=$(diff -q ./OUTPUT/createtest_client1.out ./EXPECTED/createtest_client1.exp)
DIFF2=$(diff -q ./OUTPUT/createtest_client2.out ./EXPECTED/createtest_client2.exp)

if [ "$DIFF1" == "" ]
then
    contents1=$(jq '.CreateTests.createtest_client1 |= "Passed"' testing.json) && \
    echo "${contents1}" > testing.json
fi

if [ "$DIFF2" == "" ]
then
    contents2=$(jq '.CreateTests.createtest_client2 |= "Passed"' testing.json) && \
    echo "${contents2}" > testing.json
fi

if [ "$DIFF1" == "" ] && [ "$DIFF2" == "" ]
then
    echo PASSED
else
    echo FAILED
fi

echo Create tests complete!
echo