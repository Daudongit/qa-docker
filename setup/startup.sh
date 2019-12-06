#!/bin/bash

if [ "$WEBSITE" == "chatscrum" ]; then git checkout chatscrumqa; fi

/bin/pip3.6 install -r requirements.txt
echo "*********** Testing $WEBSITE | $STAGE ***********************"
sed -i "s/environment/$STAGE/g" settings.ini
sed -i "s/website/$WEBSITE/g" settings.ini
echo "********** Currently testing  http://$STAGE.$WEBSITE.com *****"
pytest -n 4 --maillinuxjobber=True 


