#!/bin/bash
set -e
#if [ $# -ne 2 ];
#then
#    echo "Usage; ./train.sh path/to/content_img id_of_content_img"
#    echo "Example: ./train.sh content_img/c_9_face.png 9"
#    exit
#fi

read -p "Style with main face part only? 1 y 2 n: " face
if [ $face -eq 1 ];
then
    # todo_pattern="style_img/.*\_face\.png"
    # for f in $todo_pattern

    content_cnt=1
    for content in content_img/*\.png;
    do
        if [ ! -e $content ];
        then
            echo "File not exist! "
        fi
        style_cnt=1
        for style in style_img/*\_face\.png;
        do
            if [ ! -e $style ];
            then
                echo "File not exist! "
            fi
            python3 main.py --style_img $style --content_img $content --steps 25 --style_cnt $style_cnt --content_cnt $content_cnt
            style_cnt=$(($style_cnt+1))
        done
        mkdir -p output_img/c$content_cnt
        mv s*c$content_cnt*\.png output_img/c$content_cnt
        content_cnt=$(($content_cnt+1))
    done
else

    # todo_pattern="style_img/.*\.png"
    # for f in $todo_pattern;

    for f in style_img/*\.png
    do
        # dont_pattern="style_img/.*\_face\.png"
        if [ $f != style_img/*\_face\.png ];
        then
            echo "Using style: " $f
            python3 main.py --style_img $f
        fi
    done
fi
