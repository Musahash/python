import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
username = "test@707222.xyz"
password = "J%y&~wT(IM3n"
smtp_server = "mail.707222.xyz"
smtp_port = 465  # SSL port

# Email details
sender_email = "test@707222.xyz"
receiver_email = "recipient@example.com"  # Replace with the recipient's email
subject = "Test Email from Python"
body = "This is a test email sent from Python using your cPanel SMTP credentials."

# Create the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
