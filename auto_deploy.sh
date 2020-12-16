#!/bin/sh
set -x

cd ./MyBlog 
git add .
git commit -m "update blog: $1"
git push

cd ../
docker container run -it --rm --name gitbook_deploy -v `pwd`/MyBlog:/app -v `pwd`/gh-pages:/pages alfonsxh/my_gitbook 

cd ./gh-pages
git add .
git commit -m "update blog: $1"
git push

find . -name "*.md"