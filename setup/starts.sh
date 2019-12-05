#!/bin/bash
# Set environment using EXPORT ENVIRONMENT == "int" or "stage"
if [ "$WEBSITE" == "chatscrum" ]; then git checkout chatscrumqa; fi

/bin/pip3.6 install -r requirements.txt
echo "Running test for $ENVIRONMENT on $WEBSITE"
sed -i "s/environment/$ENVIRONMENT/g" settings.ini
sed -i "s/website/$WEBSITE/g" settings.ini
echo "Modified url to http://$ENVIRONMENT.$WEBSITE.com"
pytest --esend=$send --euname=$uname --epwd=$pwd --eto=$to --esubject=$subject --eorg=$org --esmtp=$smtp
# if [ "$BASIC_REPORT" == "TRUE" ]
# then
# else
#     pytest -n 4 --html=report-$ENVIRONMENT-$WEBSITE.html --self-contained-html -q --disable-warnings --tb=line -s || true
#     echo "Sending mail after test"
#     /bin/python3.6 send_mails.py $ENVIRONMENT $WEBSITE
#     tail file.log
echo "Mail Sent"


