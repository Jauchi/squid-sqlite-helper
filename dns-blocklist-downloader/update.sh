#!/bin/bash

# Your lists go here, for example:
LISTS=(
# Hosts-File syntax
'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts'
# PiHole-Syntax
'https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/notserious'
'https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Streaming'
)

echo > /var/squid/block.list

it=0
for i in "${LISTS[@]}"
do
   :
   it="$(($it+1))"
   echo "Downloading: ""$i"
   wget "$i" -O - | grep -v \
				-e '^$' \
				-e '^::1' \
				-e '#' \
				-e '^127.0.0.1' \
				-e '^255.255.255.255' \
				-e '^ff00::0' \
				-e '^fe80::1%lo0' \
				-e '^ff02::1' \
				-e '^ff02::2' \
				-e '^ff02::3' \
				-e '0.0.0.0 0.0.0.0' \
	      | sed -e 's/0.0.0.0 //g' -e 's/\^$//g' -e 's/||//g'>> /var/squid/block.list
done

chown proxy /var/squid/block.list