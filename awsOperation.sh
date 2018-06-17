#!/bin/bash

echo $1
echo $2
echo $3
echo $4

cd ~/aws
/usr/local/bin/python3 /Users/choumori/aws/aws_operation.py $1 $2 $3 $4

exit 0
