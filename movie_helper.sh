#!/bin/bash
curr_path="$(pwd)/"
echo "Curr_Path:" $curr_path
script_path=$(cd `dirname $0`; pwd)

index=0
for i in "$@"; do
    input[index]="$i"
    index=`expr $index + 1`
done


if [ ${#input[@]} == 0 ]; then
    ls $script_path | grep .py
    exit 1
fi

index=0
for i in "${input[@]}"; do
    # if contains "./", replace "./" with curr_path, eg: "-p=./", curr_path is "/d/1" -> "-p=/d/1/"
    if [[ "$i" == *=./* ]]; then
        input[index]=${i/.\//$curr_path}
    fi

    echo "para" $index "=" ${input[$index]}
    index=`expr $index + 1`
done

input[0]=$script_path/${input[0]}.py

echo "run cmd:" 
echo "python ${input[@]}"
python "${input[@]}"