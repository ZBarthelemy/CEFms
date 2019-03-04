#!/usr/bin/env bash
if [[ "$1" == "w" ]];
then
    python ./bin/cef_ms_bi_weekly.py
fi
if [[ "$1" == "d" ]];
then
    python ./bin/cef_ms_daily.py
fi