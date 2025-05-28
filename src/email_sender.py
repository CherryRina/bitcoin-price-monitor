import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender():
    def __init__(self, src_email, src_email_password, dst_email, json_loader, logger):
        self.src_email = src_email
        self.src_email_password = src_email_password
        self.dst_email = dst_email
        self.json_loader = json_loader
        self.logger = logger


    def find_max_price(self) -> str:
        """ 
        Method looks for highst price value inside a json dictionary
        Returns sentance with the value
        """
        json_data = self.json_loader.json_data
        if not json_data:
            return "Could not determine max Bitcoin price."
        last_60_items = dict(list(json_data.items())[-30:])
        max_row = max(last_60_items, key=lambda x: last_60_items[x])
        price = f"{last_60_items[max_row]:,}"
        result = f"Maximum Bitcoin price in the past hour was ${price} at {max_row}."
        return result


    def create_message(self, title: str, message:str) -> str:
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


    def send_email(self, email_letter:str) -> None: 
        """
        Recieves a string email letter and sends it to the destination email
        Logs final status
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
            self.logger.info(f"An email was sent to '{self.dst_email}'")
        except Exception as e:
            self.logger.error(f"Failed to send email: '{e}'")

