#!/bin/bash
problem=""
if [ "$1" == "" ]; then
    echo "problem not given"
    exit 1
fi
problem=$1
if [ "$2" == "create" ]; then
    if [ -f "$problem.cpp" ]; then
        echo "already exist"
        exit 1
    fi
    echo "#include <iostream>" > "$problem.cpp"
    echo "using namespace std;" >> "$problem.cpp"
    echo "" >> "$problem.cpp"
    echo "int main(){" >> "$problem.cpp"
    echo "    ios::sync_with_stdio(false);" >> "$problem.cpp"
    echo "    cin.tie(NULL);" >> "$problem.cpp"
    echo "    int t;" >> "$problem.cpp"
    echo "    cin>>t;" >> "$problem.cpp"
    echo "    for(int t_i=0;t_i<t;t_i++){" >> "$problem.cpp"
    echo "        " >> "$problem.cpp"
    echo "    }" >> "$problem.cpp"
    echo "}" >> "$problem.cpp"
    echo "" > "$problem.input"
    echo "created"
    exit 0
fi
if [ "$2" == "run" ]; then
    if [ ! -f "$problem" ]; then
        echo "not compiled yet"
        exit 1
    fi
    if [ ! -f "$problem.input" ]; then
        echo "input file not ready"
        echo "" > "$problem.input"
        echo "input file created"
        exit 1
    fi
    echo running problem: $problem
    start=$(date +%s)
    "./$problem" < "$problem.input" > "$problem.output"
    ret_code=$?
    echo executed in $(( $(date +%s) - $start ))s
    echo terminated returning $ret_code
    exit 0
fi
if [ ! -f "$problem.cpp" ]; then
    echo "problem not found"
    exit 1
fi
echo compiling problem $problem:
g++ -std=c++17 "$problem.cpp" -o "$problem"
if [ ! -f "$problem" ]; then
    exit 1
fi
if [ ! -f "$problem.input" ]; then
    echo "input file not ready"
    echo "" > "$problem.input"
    echo "input file created"
    exit 1
fi
echo compilation done!
echo running:
start=$(date +%s)
"./$problem" < "$problem.input" > "$problem.output"
ret_code=$?
echo executed in $(( $(date +%s) - $start ))s
echo terminated returning $ret_code
exit 0
