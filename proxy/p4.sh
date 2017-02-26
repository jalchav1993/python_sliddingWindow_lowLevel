#!/bin/bash
python udpProxy.py --clientPort 50000 --serverAddr localhost:50001 --byteRate 10000 --propLat .05 --qCap 1 --pDrop 0.5 --pDelay 0.25 --verbose
