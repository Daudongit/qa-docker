import sys
import smtplib
import logging
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from email.mime.text import MIMEText


parser = ConfigParser()
parser.read('settings.ini')

def get_logger(log_name):
    logger = logging.getLogger(log_name)
    f_handler = logging.FileHandler('file.log')
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.setLevel(logging.INFO)
    return logger

def send_email_ses(
    recipients,site,
    username=parser.get('mail', 'username'),
    password=parser.get('mail', 'password'),
    from_address=parser.get('mail', 'sender')):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = recipients
    msg['Subject'] = "Test Notification: {}".format(site.upper())

    try:
        with open('report.{}.html'.format(site), 'r') as stream:
            data = "{}".format(BeautifulSoup(stream.read(),features='lxml'))
            data = data.replace('\n', '').replace('\r', '')
            html = data
            body = 'Test results for {}'.format(site)

            msg.attach(MIMEText(body, 'plain'))
            msg.attach(MIMEText(html, 'html'))

            server = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com', 587)
            server.starttls()
            server.login(username, password)
            text = msg.as_string()
            server.sendmail(from_address, recipients.split(','), text)
            server.quit()
            logger = get_logger('Mailing')
            logger.info('Mail Sent')
    except Exception as e:
        logger = get_logger('Mailing')
        logger.info('Mail Not Sent: \n {}'.format(e))
        # print('Mail Not Sent: \n {}'.format(e))


def send():
    if len(sys.argv) < 3:
        print("Wrong format")
        print("Usage: send_mail.py int.linuxjobber.com")
        sys.exit(1)
    else:
        site = sys.argv[1]
        recipient_list = parser.get('mail', 'recipients')
        send_email_ses(recipient_list,site)

if __name__ == "__main__":
    send()