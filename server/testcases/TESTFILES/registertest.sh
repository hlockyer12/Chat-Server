#!/bin/bash

coverage run ../server.py 2040 &
sleep 1

python3 ../client.py 2040 INPUT/registertest_client1.in > ./OUTPUT/registertest_client1.out &
sleep 2

python3 ../client.py 2040 INPUT/registertest_client2.in > ./OUTPUT/registertest_client2.out &
sleep 2

DIFF1=$(diff -q ./OUTPUT/registertest_client1.out ./EXPECTED/registertest_client1.exp)
DIFF2=$(diff -q ./OUTPUT/registertest_client2.out ./EXPECTED/registertest_client2.exp)

# The first test to complete will pull the initial state of the json file
# from the initialstate.json file.
# DO NOT EDIT OR CHANGE THIS FILE
if [ "$DIFF1" == "" ]
then
    contents1=$(jq '.RegisterTests.registertest_client1 |= "Passed"' testing.json) && \
    echo "${contents1}" > testing.json
fi

if [ "$DIFF2" == "" ]
then
    contents2=$(jq '.RegisterTests.registertest_client2 |= "Passed"' testing.json) && \
    echo "${contents2}" > testing.json
fi

if [ "$DIFF1" == "" ] && [ "$DIFF2" == "" ]
then
    echo PASSED
else
    echo FAILED
fi


echo Register tests complete!
echo