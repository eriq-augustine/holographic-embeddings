#!/bin/sh

python kg/run_hole.py --fin data/fb15k.bin \
       --test-all 50 --nb 100 --me 500 \
       --margin 0.2 --lr 0.1 --ncomp 150
