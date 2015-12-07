#!/bin/bash
sed 's/^/0/;s/)/-1/g;s/(/+1/g' | bc
