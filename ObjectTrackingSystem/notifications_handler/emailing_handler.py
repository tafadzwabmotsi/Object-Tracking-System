__author__ = "Tafadzwa Brian Motsi"

import sys
import shutil
import os

sys.path.append("..")

from .authentication import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailingHandler:
    def __init__(self, recipient, path_to_image):
        self.recipient = recipient
        self.path_to_image = path_to_image
        self.copied_image_name = None

    def copy_image_to_current_dir(self):
        image_name = str(self.path_to_image).split('/')[-1]

        if image_name is not None:
            self.copied_image_name = image_name
            shutil.copyfile(self.path_to_image, str(os.getcwd()) + '/' + image_name)
        else:
            pass

        return image_name

    def send_email(self, subject, body_content):
        msg = MIMEMultipart()

        # prepare an email
        msg['From'] = user_name
        msg['To'] = self.recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body_content, 'plain'))

        # attach an image
        image_name = self.copy_image_to_current_dir()

        if image_name is not None:
            image_data = open(str(image_name), 'rb').read()
            image = MIMEImage(image_data, name=os.path.basename(str(image_name)))
            msg.attach(image)

            os.remove(str(image_name))

            # send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                try:
                    print('sending...')
                    smtp.login(user_name, password)
                    smtp.send_message(msg)
                    print('email message sent successfully...')
                except Exception as e:
                    print(e)

        else:
            print('could not attach image...')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                try:
                    print('sending...')
                    smtp.login(user_name, password)
                    smtp.send_message(msg)
                    print('email message sent successfully...')
                except Exception as e:
                    print(e)
