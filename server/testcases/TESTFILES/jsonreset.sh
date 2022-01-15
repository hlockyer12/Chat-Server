#!/bin/bash

# This script will reset the state of json file containing results of the test

contents=$(jq . ./TESTFILES/initialstate.json) && \
echo "${contents}" > testing.json