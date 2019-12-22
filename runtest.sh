#!/bin/bash

WEBSITE=$1

sed -i "s/website/$WEBSITE/g" setup/settings.ini

# sudo docker container create 
docker create  --name qa-test qa-s

docker cp $(pwd)/test/qa/. qa-test:/qa

docker cp $(pwd)/setup/settings.ini qa-test:/qa/settings.ini

docker start qa-test 

docker exec  qa-test echo "********** Currently testing $WEBSITE *****" && pytest -n 1 --maillinuxjobber=True