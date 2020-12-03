from django.core.mail import EmailMessage
import os
import smtplib
import yagmail

# class Util:
#     @staticmethod
#     def send_email(data):

#         email = EmailMessage(subject=data['email_subject'],body=data['email_body'],to=[data['to_email']])
#         email.send()

# class Util:
#     @staticmethod
#     def send_email(data):
#         s = smtplib.SMTP('smtp.gmail.com', 587)
#         s.starttls()
#         s.login("shubhakshat10@gmail.com", "Gupta2002")
#         s.sendmail("shubhakshat10@gmail.com", data['to_email'], data['email_body'])
#         s.quit()

class Util:
    @staticmethod
    def send_email(data):
        yag = yagmail.SMTP(user=os.environ.get('EMAIL_HOST_USER'), password=os.environ.get('EMAIL_HOST_PASSWORD'))
        yag.send(to=data['to_email'], subject=data['email_subject'], contents=data['email_body'])


# try:
#     yag = yagmail.SMTP(user='my_username@gmail.com', password='mypassword')
#     yag.send(to='recipient_username@gmail.com', subject='Testing Yagmail', contents='Hurray, it worked!')
#     print("Email sent successfully")
# except:
#     print("Error, email was not sent")
