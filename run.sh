#!/bin/bash

myscript(){
    python3 ./quickstart.py
}

until myscript; do
    echo "'quickstart.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done