#!/bin/bash
problem="2131E"
echo compiling:
g++ -std=c++17 "$problem.cpp" -o "$problem"
echo compilation done!
echo running:
start=$(date +%s)
"./$problem" < "$problem.input" > "$problem.output"
ret_code=$?
echo executed in $(( $(date +%s) - $start ))s
echo terminated returning $ret_code