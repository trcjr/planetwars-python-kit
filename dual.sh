#!/bin/bash
# runs MyBot against DualBot sample bot
# pass map # as a parameter, for instance dual.sh 1
java -jar tools/PlayGame.jar maps/map$1.txt 1000 200 log.txt "java -jar example_bots/DualBot.jar" "python MyBot.py --log MyBot.log" | python visualizer/visualize_localy.py 
