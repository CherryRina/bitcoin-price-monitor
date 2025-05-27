import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender():
    def __init__(self, src_email, src_email_password, dst_email, logger):
        self.src_email = src_email
        self.src_email_password = src_email_password
        self.dst_email = dst_email
        self.logger = logger


    def create_message(self, title, message):
        """ 
        Recieves two strings - title and message 
        Returns a ready email letter as string
        """
        email_letter = MIMEMultipart()
        email_letter["Subject"] = title
        email_letter["From"] = self.src_email
        email_letter["To"] = self.dst_email
        email_letter.attach(MIMEText(message, "plain"))
        return email_letter.as_string()


    def send_email(self, email_letter):
        """
        Recieves a string email letter and sends it to the destination email
        Prints final status
        """
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:                     
                connection.starttls()    
                connection.login(user=self.src_email, password=self.src_email_password)    
                connection.sendmail(                                               
                    from_addr=self.src_email,
                    to_addrs=self.dst_email,
                    msg=email_letter
            ) 
            self.logger.info(f"An email was sent to {self.dst_email}")
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")

