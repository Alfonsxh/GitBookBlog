#/bin/sh

cd ./master 
git add .
git commit -m "update blog: $1"
git push

# cd ../
docker container run -it --rm --name gitbook_deploy -v `pwd`/master:/app -v `pwd`/gh-pages:/pages my_gitbook

# cd ./gh-pages
# git add .
# git commit -m "update blog: $1"
# git push