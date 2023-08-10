#!/bin/bash

server_name="flask_server.py"
for p in `pgrep -f ${server_name}`; do
    kill -9 $p
done
nohup python3 "${server_name}" > /dev/null &
