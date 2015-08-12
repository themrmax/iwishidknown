#!/bin/bash
aws s3 cp s3://iwishidknown/iwishidknown.py ./
aws s3 cp s3://iwishidknown/watchlist.txt ./
python iwishidknown.py
