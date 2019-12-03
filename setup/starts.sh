#!/bin/bash
# Set environment using EXPORT ENVIRONMENT == "int" or "stage"
/bin/pip3.6 install -r requirements.txt
echo "Running test for $ENVIRONMENT on $SITE"
sed -i "s/environment/$ENVIRONMENT/g" settings.ini
sed -i "s/site/$SITE/g" settings.ini
echo "Modified url to http://$ENVIRONMENT.$SITE.com"
pytest -n 4 --html=report-$ENVIRONMENT-$SITE.html --self-contained-html -q --disable-warnings --tb=line -s || true
echo "Sending mail after test"
/bin/python3.6 send_mails.py $ENVIRONMENT $SITE
tail file.log
echo "Mail Sent"


