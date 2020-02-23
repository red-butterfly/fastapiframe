# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-18
@function:
send email by async sample
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from utils.tools import datetime2str


_logger = None
_email_sender = ''
_email_receivers = ['']
_app_name = 'FlaskFrame'
_html_format = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">

  <title></title>

  <style type="text/css">
  </style>
</head>
<body style="margin:0; padding:0; background-color:#F2F2F2;">
  <center>
   <br />
    <h3><font color="red"> 🕷 Get Error Logger From FlaskFrame 🕷 </font></h3>
    <br />
    <table width="640" cellspacing="0" cellpadding="0" border="1" align="center" style="border: #00AEAE solid 1px;max-width:640px; width:100%;" bgcolor="#FFFFFF">
        <tr>
            <td align="center" valign="top" style="padding:10px;">
                 🔗 Monitor URL:
            </td>
            <td align="left" valign="top" style="padding:10px;">
                {url}
            </td>
        </tr>
        <tr>
            <td align="center" valign="top" style="padding:10px;">
                 ⏰ Time:
            </td>
            <td align="left" valign="top" style="padding:10px;">
                {time}
            </td>
        </tr>
        <tr>
            <td align="center" valign="top" style="padding:10px;">
                 📜 LogInfo:
            </td>
            <td align="left" valign="top" style="padding:10px;">
                <p>{log}</p>
            </td>
        </tr>
      </table>
      <br />
      <br />
      <br />
  </center>
</body>
</html>
'''


def set_emailsetting(logger, app_name, receivers=None):
    '''
    init send email
    :param logger:
    :param app_name:
    :param receivers:
    :return:
    '''
    global _logger, _app_name, _email_receivers
    _logger = logger
    _app_name = app_name
    if receivers:
        _email_receivers = receivers
    if _logger:
        _logger.info('Init SendEmail')


def send_email(subject, sendtext, errinfo):
    '''
    send email
    :param subject:  title
    :param sendtext:  content
    :return:
    '''
    message = MIMEText(_html_format.format(url=errinfo[0] ,time=datetime2str(), log=sendtext), 'html', 'utf-8')
    message['From'] = formataddr(['Logger-{0}'.format(_app_name), _email_sender])
    message['Subject'] = Header(subject, 'utf-8')  # 邮件的主题

    smtpObj = smtplib.SMTP_SSL('smtp.exmail.qq.com', port=465)
    smtpObj.login(user=_email_sender, password='P2Jw8rtWDzWkHJPo')  # password并不是邮箱的密码，而是开启邮箱的授权码
    smtpObj.sendmail(_email_sender, _email_receivers, message.as_string())  # 发送邮件
    if _logger:
        _logger.info('Have send email to <{0}>'.format(','.join(_email_receivers)))







