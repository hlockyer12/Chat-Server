#!/bin/bash

coverage run ../server.py 3000 &
sleep 1
coverage run ../server.py > ./OUTPUT/othertest.out 2>&1
sleep 1
coverage run ../server.py 3000 >> ./OUTPUT/othertest.out 2>&1

DIFF1=$(diff -q ./OUTPUT/othertest.out ./EXPECTED/othertest.exp)

if [ "$DIFF1" == "" ]
then
    contents1=$(jq '.OtherTests.othertest |= "Passed"' testing.json) && \
    echo "${contents1}" > testing.json
    echo PASSED
else
    echo FAILED
fi

echo Other tests complete!
echo