#!/bin/bash

# while IFS="===" read -r ip community; do
while read line;do
  ip=`echo $line|awk -F "===" '{print $1}'`
  community=`echo $line|awk -F "===" '{print $2}'`
  echo $ip
  echo $community
  snmp_result=$(timeout 1  snmpwalk -v2c -c "$community" "$ip" sysname  2>&1 && echo "ok" || echo "fail")
  #ping_result=$(timeout 1 ping -c 1 "$ip" > /dev/null 2>&1 && echo "ok" || echo "fail")

  echo "$ip Ping result: $ping_result snmp result: $snmp_result"

  echo "-------------------"
done < iprantext.txt
