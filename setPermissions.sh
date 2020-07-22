#!/bin/bash
echo -e "PLEASE ENUSRE YOU RUN THIS IN THE END(THIS FILL WILL DELETE ITSELF!)"
echo -e "Are you sure you want to proceed?(y/n)\c"
read n
if [ $n = 'y' ]
then
    chmod 000 [!_]*
    mkdir -m=200 __pycache__
    chmod 200 __pycache__
    chmod 500 ./*.py
    chmod 400 *.md
    chmod 600 *.log
    rm -rf setPermissions.sh
fi
