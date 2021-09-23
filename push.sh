#!/usr/bin/env bash


#git rm -r --cached .


read -p "Commit description: " desc

git add .
git commit -m "$desc"
git push -u origin master

git status
            
