#!/bin/bash

if [ "$WEBSITE" == "chatscrum" ]; then git checkout chatscrumqa; fi

/bin/pip3.6 install -r requirements.txt
echo "*********** Testing $WEBSITE | $STAGE ***********************"
sed -i "s/environment/$STAGE/g" settings.ini
sed -i "s/website/$WEBSITE/g" settings.ini
echo "********** Currently testing  http://$STAGE.$WEBSITE.com *****"
pytest --mail-linuxjobber=True
echo "*********** Sending mail after test ***************************"
#     pytest -n 4 --html=report-$STAGE-$WEBSITE.html --self-contained-html -q --disable-warnings --tb=line -s || true
#     echo "Sending mail after test"
#     /bin/python3.6 send_mails.py $STAGE $WEBSITE
#     tail file.log
echo "Mail Successfully Sent"


