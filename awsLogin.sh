#!/bin/sh
hostdefault="52.68.76.91"
user="ec2-user"

if [ "$1" == "jupyter" ] || [ "$1" == "web" ]
then 
  echo "connect to $1 server"
  cd ~/aws
  /usr/local/bin/python3 ~/aws/awsLogin.py $1
  exit 0
elif [ "$1" ] 
then
  echo "connect to server:$1"
  host=$1
else 
  echo "connect to default: $hostdefault"
  host=$hostdefault
fi

echo "v1:$1, v2:$2"

if [ "$2" == "ubuntu" ]
then
  user=$2
fi

echo "connect to $user@$host"
ssh -i ~/.ssh/stock-tokyo.pem $user@$host
