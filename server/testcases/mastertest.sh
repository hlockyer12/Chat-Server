#!/bin/bash

echo '#########################'
echo '#  CHAT SERVER TESTING  #'
echo '#########################'
coverage erase # Remove all previous .coverage files
./TESTFILES/jsonreset.sh
echo
echo Starting register tests...
./TESTFILES/registertest.sh

echo Starting login tests...
./TESTFILES/logintest.sh

echo Starting create tests...
./TESTFILES/createtest.sh

echo Starting join tests...
./TESTFILES/jointest.sh

echo Starting channels tests...
./TESTFILES/channelstest.sh

echo Starting say tests...
./TESTFILES/saytest.sh

echo Starting other tests...
./TESTFILES/othertest.sh

echo All tests complete!
echo

killall -2 coverage # Send SIGINT to all coverage processes to exit them gracefully
killall -2 python3 # Send SIGINT to all python3 processes to exit them gracefully

sleep 4
coverage combine
coverage html
echo
coverage report
echo
echo '#########################'
echo '#        GOODBYE        #'
echo '#########################'