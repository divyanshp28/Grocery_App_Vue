from datetime import datetime, timedelta
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from src import celery, sender_email, mailhog_host, mailhog_port, app
from src.models import Order, User
from celery.schedules import crontab

@celery.task(name='app.send_daily_reminder_task')
def send_daily_reminder_task():
    try:
        # Calculate the date for one day ago
        one_day_ago = datetime.utcnow() - timedelta(days=1)

        # Query all users who haven't visited the website in the one days
        users = User.query.filter(User.last_active < one_day_ago).all()
        if len(users) == 0:
            magenta = '\033[95m' 
            RESET = '\033[0m'
            message = f"{magenta}-----------------Email not sent to anyone everyone was active------------------\n Task execution successful-{RESET}"
            return {"message":message}
        # users = User.query.all()

        # users = [{'email':'abc@gmail.com'}]


        for user in users:
            # email = user['email']
            email = user.email

            # print(f"Sending weekly reminder to user: {user['email']}") #{user.name}
            print(f"Sending weekly reminder to user: {user.email}") #{user.name}

            # Customize the reminder message as needed
            # reminder_message = f"Hello {user['email']},\n\nWe hope you're doing well! " \
            reminder_message = f"Hello {user.username},\n\nWe hope you're doing well! " \
                               f"It looks like you haven't visited our website today. " \
                               f"We invite you to check out the latest deals in groceries. " \
                               f"\n\nBest regards,\nGroceryApp"

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = 'Daily Reminder from GroceryApp'

            msg.attach(MIMEText(reminder_message, 'plain'))

            print(f"Sending email to {email}...")

            # Connect to MailHog's SMTP server
            with smtplib.SMTP(mailhog_host, mailhog_port) as server:
                # Send the email
                server.sendmail(sender_email, [email], msg.as_string())
                print(f"Email sent successfully to {email}")

        return {'message': 'Daily reminders sent successfully to users'}
    
    except Exception as e:
        error_message = f"Error sending daily reminders: {str(e)}"
        print(error_message)
        return {'message': 'Failed to send daily reminders to users'}, 500
    
########################################################################################
    ######################### MONTHLY REPORT #######################################

@celery.task(name='app.send_monthly_report_task')
def send_monthly_report_task():
    last_month = datetime.utcnow() - timedelta(days=30)

    users = User.query.all()

    user_order_count = {}
    for user in users:
        orders_last_month = Order.query.filter_by(user_id=user.id).filter(Order.order_date >= last_month).all()
        order_count = len(orders_last_month)
        email = user.email

        # print(f"Sending weekly reminder to user: {user['email']}") #{user.name}
        print(f"Sending weekly reminder to user: {user.email}") #{user.name}

        # Customize the reminder message as needed
        reminder_message = f"Hello {user.username},\n\nWe hope you're doing well! " \
                            f"Here is your monthly shopping report. " \
                            f"You have made {order_count} orders in the last month. " \
                            f"\n\nBest regards,\nGroceryApp"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Monthly Report from GroceryApp'

        msg.attach(MIMEText(reminder_message, 'plain'))

        print(f"Sending email to {email}...")

        # Connect to MailHog's SMTP server
        with smtplib.SMTP(mailhog_host, mailhog_port) as server:
            # Send the email
            server.sendmail(sender_email, [email], msg.as_string())
            print(f"Email sent successfully to {email}")

        return {'message': 'Monthly report sent successfully to users'}

celery.conf.timezone = 'Asia/Kolkata'
    
