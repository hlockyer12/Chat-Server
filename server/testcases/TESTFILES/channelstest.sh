#!/bin/bash

coverage run ../server.py 2080 &
serverid=$!
sleep 1

python3 ../client.py 2080 INPUT/channelstest_client1.in > ./OUTPUT/channelstest_client1.out &
sleep 2

python3 ../client.py 2080 INPUT/channelstest_client2.in > ./OUTPUT/channelstest_client2.out &
sleep 2

DIFF1=$(diff -q ./OUTPUT/channelstest_client1.out ./EXPECTED/channelstest_client1.exp)
DIFF2=$(diff -q ./OUTPUT/channelstest_client2.out ./EXPECTED/channelstest_client2.exp)

if [ "$DIFF1" == "" ]
then
    contents1=$(jq '.ChannelsTests.channelstest_client1 |= "Passed"' testing.json) && \
    echo "${contents1}" > testing.json
fi

if [ "$DIFF2" == "" ]
then
    contents2=$(jq '.ChannelsTests.channelstest_client2 |= "Passed"' testing.json) && \
    echo "${contents2}" > testing.json
fi

if [ "$DIFF1" == "" ] && [ "$DIFF2" == "" ]
then
    echo PASSED
else
    echo FAILED
fi

echo Channels tests complete!
echo