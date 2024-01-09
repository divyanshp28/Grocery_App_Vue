from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery.schedules import crontab
from redis import Redis
from src import celery_config
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
api = Api(app)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///groceryapp.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key="secret@1234"

db=SQLAlchemy(app)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
celery = celery_config.make_celery(app)

mail = Mail(app)

# MailHog configuration
mailhog_host = '127.0.0.1'
mailhog_port = 1025

# Sender and recipient information
sender_email = 'wedemonic@gmail.com'
# recipient_email = 'recipient@example.com'

# Create a message
# subject = 'Hello from MailHog via smtplib'
# body = 'This is a test email from smtplib with MailHog.'
# message = MIMEText(body)
# message['Subject'] = subject
# message['From'] = sender_email
# message['To'] = recipient_email

# # Connect to MailHog's SMTP server
# with smtplib.SMTP(mailhog_host, mailhog_port) as server:
#     # Send the email
#     server.sendmail(sender_email, [recipient_email], message.as_string())

# print("Email sent successfully!")


from src.routes.Auth import store_admin_auth, super_admin_auth, user_auth
from src.routes import admin, store_admin, store_admin_requests, user,category, product, cart, cartitem, order

from src.celery_workers import send_daily_reminder_task, send_monthly_report_task

celery.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'app.send_daily_reminder_task',
        'schedule': crontab(hour=16, minute=2, day_of_week='*')
        # 'schedule': crontab(minute='*/1')
    },
    'send-monthly-engagement-report': {
        'task': 'app.send_monthly_report_task',
        'schedule': crontab(day_of_month='1', hour=10, minute=0)
        # 'schedule': crontab(minute='*/1')
    }
}