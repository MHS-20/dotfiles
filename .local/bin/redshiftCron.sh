#!/bin/bash

CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -ge 19 ]; then    
    /usr/bin/redshift -P -O 3000 > /dev/null 2>&1
else 
   /usr/bin/redshift -x > /dev/null 2>&1
fi
