#! /bin/bash

function del_zip(){
	    cd $1
            rm -rf *.zip
            cd ..
}

function read_dir(){
    for file in `ls $1`
    do
        if [ -d $1"/"$file ]
        then
	    del_zip $1"/"$file
            read_dir $1"/"$file
        fi
    done
}

function release(){
    for file in `ls $1`
    do
        if [ -d $1"/"$file ]
        then
	   cd $1"/"$file
	   python release.py
	   cd ..
        fi
    done
}



CUR_DIR=`pwd`
read_dir $CUR_DIR
python release.py
