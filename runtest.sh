#!/bin/bash

WEBSITE="url:${1:-"https://int.linuxjobber.com"}"
IMAGE=${2:-"qaserver"}
# CONTAINER="${WEBSITE/"url:https://"/""}" 
# CONTAINER="${CONTAINER//"."/""}" 
CONTAINER=$(echo "$WEBSITE"|sed 's/url:https:\/\///g')
# CONTAINER=$(echo "$CONTAINER"|sed 's/.//g')

sed -i "/url/c $WEBSITE" setup/settings.ini
# find $(pwd)/setup/ -name '*.ini' -print0 | xargs -0 sed -i "s/website/$WEBSITE/g"

# sudo docker container create 
docker rm $CONTAINER -f || echo "No previous container" && docker create  --name $CONTAINER $IMAGE

docker cp $(pwd)/test/qa/. $CONTAINER:/qa

docker cp $(pwd)/setup/settings.ini $CONTAINER:/qa/settings.ini

docker start $CONTAINER 

docker exec  $CONTAINER pytest -n 1 --maillinuxjobber=True