#!/bin/bash

set_args(){
    for ARGUMENT in "$@"
    do
        KEY=$(echo $ARGUMENT | cut -f1 -d=)
        VALUE=$(echo $ARGUMENT | cut -f2 -d=)   

        case "$KEY" in
                WEBSITE)              WEBSITE=${VALUE} ;;
                DOCKER_IMAGE)    DOCKER_IMAGE=${VALUE} ;;     
                FULL_REPORT)      FULL_REPORT=${VALUE} ;;     
                *)   
        esac    
    done
}

container_not_exit(){
    docker_output=$( docker rm $CONTAINER -f 2>&1)
    [[ $docker_output == *"No such container"* ]]
}

WEBSITE="https://int.linuxjobber.com"
DOCKER_IMAGE="qaserver"
FULL_REPORT="False"

set_args $@

FULL_REPORT="$(echo $FULL_REPORT| tr [a-z] [A-Z])"
URL="url:$WEBSITE"
CONTAINER=$(echo "$WEBSITE"|sed 's/https:\/\///g')

sed -i "/url/c $URL" setup/settings.ini

if container_not_exit; then
    echo "No previous container"
else
    echo "Previous container removed"
fi

docker create  --name $CONTAINER $DOCKER_IMAGE

docker cp $(pwd)/test/qa/. $CONTAINER:/qa

docker cp $(pwd)/setup/settings.ini $CONTAINER:/qa/settings.ini

docker start $CONTAINER 

echo "********** Currently testing  $WEBSITE *****"

if [ "$FULL_REPORT" == "TRUE" ]; then
    docker exec  $CONTAINER  /bin/bash -c "\
    pytest -n 4 --html=report.$CONTAINER.html --self-contained-html -q --disable-warnings --tb=line -s || true && \
    echo 'Sending mail after test' && \
    python3.6 send_mails.py $CONTAINER && \
    tail file.log"
else
    docker exec  $CONTAINER pytest -n 1 --maillinuxjobber=True
fi
exit 0