from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
from email.mime.text import MIMEText
import pytest
import time
import smtplib
import datetime
import platform

execution_date = "Today"

def pytest_addoption(parser):
    parser.addoption(
        '--maillinuxjobber',
        action='store',
        dest='maillinuxjobber',
        default='False',
        help='Test mail to liuxjobber'
    )


def pytest_sessionstart(session):
    global execution_date
    execution_date = datetime.datetime.now().strftime("%b %d %Y, %H:%M")

@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    duration = time.time() - terminalreporter._sessionstarttime
    yield
    test_info = {}
    test_info['passed'] = len(terminalreporter.stats.get('passed', ""))
    test_info['failed'] = len(terminalreporter.stats.get('failed', ""))
    test_info['skipped'] = len(terminalreporter.stats.get('skipped', ""))
    test_info['error'] = len(terminalreporter.stats.get('error', ""))
    test_info['xfailed'] = len(terminalreporter.stats.get('xfailed', ""))
    test_info['xpassed'] = len(terminalreporter.stats.get('xpassed', ""))

    test_info['total'] = sum(test_info.values())
    test_info['percentage'] = round(test_info['passed']*100.0/test_info['total'],2)
    test_info['execution_date'] = execution_date
    test_info['elapsed_time'] = duration

    if config.option.maillinuxjobber == "True":
        send_email(test_info)

def send_email(test_info):
    server = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com', 587)
    config = _get_param()
    recipient_list = config['recipient_list']
    from_user = config['sender']
    msg = MIMEMultipart()
    msg['Subject'] = 'Test Result of:'+config['tested_site']+' as of '+test_info['execution_date']
    msg['From'] = from_user
    msg['To'] = recipient_list

    # msg.add_header('Content-Type', 'text/html')
    email_content = _get_email_content(test_info,config['org'])
    msg.attach(MIMEText(email_content, 'html'))

    server.starttls()
    server.login(config['username'], config['password'])
    server.sendmail(from_user, recipient_list, msg.as_string())


#Helper
def _get_param():
    parser = ConfigParser()
    parser.read('settings.ini')
    
    return {
        'username':parser.get('mail', 'username'),
        'password':parser.get('mail', 'password'),
        'sender':parser.get('mail', 'sender'),
        'recipient_list':parser.get('mail', 'recipients'),
        'tested_site':parser.get('site_to_test', 'url'),
        'org':'Linuxjobber'
    }

def _get_email_content(test_info,organization):
    return """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>Automation Status</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0 " />
        <style>
            .rf-box {
                max-width: 60%%;
                margin: auto;
                padding: 30px;
                border: 3px solid #eee;
                box-shadow: 0 0 10px rgba(0, 0, 0, .15);
                font-size: 16px;
                line-height: 28px;
                font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
                color: #555;
            }
            
            .rf-box table {
                width: 100%%;
                line-height: inherit;
                text-align: left;
            }
            
            .rf-box table td {
                padding: 5px;
                vertical-align: top;
                width: 50%%;
                text-align: center;
            }
            
            .rf-box table tr.heading td {
                background: #eee;
                border-bottom: 1px solid #ddd;
                font-weight: bold;
                text-align: left;
            }
            
            .rf-box table tr.item td {
                border-bottom: 1px solid #eee;
            }
        </style>
    </head>
    <body>
        <div class="rf-box">
            <table cellpadding="0" cellspacing="0">
                <tr class="top">
                    <td colspan="2">
                        <table>
                            <tr>
                                <td></td>
                                <td style="text-align:middle">
                                    <h1>%s</h1>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            <p style="padding-left:20px">
                Hi Team,<br>
                Following are the last build execution result.
            </p>
            <table style="width:80%%;padding-left:20px">
                <tr class="heading">
                    <td>Test Status</td>
                    <td></td>
                </tr>
                <tr class="item">
                    <td>Total</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>Pass</td>
                    <td style="color:green">%s</td>
                </tr>
                <tr class="item">
                    <td>Fail</td>
                    <td style="color:red">%s</td>
                </tr>
                <tr class="item">
                    <td>Skip</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>Error</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>xPassed</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>xFailed</td>
                    <td>%s</td>
                </tr>
            </table>
            <br>
            <table style="width:80%%;padding-left:20px">
                <tr class="heading">
                    <td>Other Info:</td>
                    <td></td>
                </tr>
                <tr class="item">
                    <td>Pass Percentage (%%)</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>Executed Date</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>Machine</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>OS</td>
                    <td>%s</td>
                </tr>
                <tr class="item">
                    <td>Duration(s)</td>
                    <td>%s</td>
                </tr>
            </table>
            <table>
                <tr>
                    <td style="text-align:center;color: #999999; font-size: 11px">
                        <p>Best viewed in web!</p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """ % ( organization,test_info['total'],test_info['passed'],test_info['failed'],
            test_info['skipped'],test_info['error'],test_info['xpassed'],
            test_info['xfailed'],test_info['percentage'],test_info['execution_date'],
            platform.uname()[1], platform.uname()[0],test_info['elapsed_time'])