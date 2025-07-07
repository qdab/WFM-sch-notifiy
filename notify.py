import os
import smtplib
from datetime import date
from email.message import EmailMessage

from server import load_schedule

SMTP_HOST = os.environ.get('SMTP_HOST', 'localhost')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '25'))
FROM_ADDR = os.environ.get('FROM_ADDR', 'noreply@example.com')
TO_ADDR = os.environ.get('TO_ADDR', 'user@example.com')


def send_email(subject, body, to_addr=TO_ADDR):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_ADDR
    msg['To'] = to_addr
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.send_message(msg)


def notify_today():
    today = date.today().isoformat()
    entries = load_schedule()
    for e in entries:
        if e['date'] == today:
            send_email(f"Task for {today}", e['task'])


if __name__ == '__main__':
    notify_today()
