#!/bin/bash

while IFS="===" read -r ip community; do
  snmp_result=$(timeout 1  snmpwalk -v2c -c "$community" "$ip" sysname  2>&1 && echo "ok" || echo "fail")
  ping_result=$(timeout 1 ping -c 1 "$ip" > /dev/null 2>&1 && echo "ok" || echo "fail")
#   snmp_result=$(timeout 2  snmpwalk -v2c -c "$community" "$ip" sysname > /dev/null 2>&1 && echo "ok" || echo "fail")
#    timeout 1 snmpwalk -v2c -c $ro $ip sysname ; 

  echo "$ip Ping result: $ping_result snmp result: $snmp_result"

  echo "-------------------"
done < ipran.txt

# snmp result: ok


# 4.76.141.3===RRnGdsa&1msH
# 4.76.229.2===CTz5a%jz

# timeout 1 snmpwalk -v2c -c "RRnGdsa&1msH" "4.76.141.3" sysname > /dev/null 2>&1 && echo "ok" || echo "fail";
timeout 1 snmpwalk -v2c -c "CTz5a%jz" "4.76.229.2" sysname > /dev/null 2>&1 && echo "ok" || echo "fail";
timeout 1 snmpwalk -v2c -c "RRnGdsa&1msH" "4.76.141.3" sysname 2>&1 && echo "ok" || echo "fail";