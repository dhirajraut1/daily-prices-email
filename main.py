from datetime import datetime
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Scrape the prices table
url = "https://ramropatro.com/vegetable"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='commodityDailyPrice')
    if table:
        rows = table.find_all('tr')
        
        # Compose the email content as an HTML table
        email_content = "<table style='border-collapse: collapse; width: 100%; border: 1px solid black;'><tr>"
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            email_content += "<tr>" + "".join(f"<td>{data}</td>" for data in row_data) + "</tr>"
        email_content += "</table>"
    else:
        print("Table 'commodityDailyPrice' not found.")
else:
    print("Failed to retrieve the webpage.")

print(email_content)

# Get today's date in a specific format
today_date = datetime.now().strftime("%Y-%m-%d")

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = os.environ.get("USER_EMAIL")
sender_password = os.environ.get("USER_PASSWORD")

# Read recipient email addresses from the JSON file
with open("recipients.json", "r") as json_file:
    data = json.load(json_file)
    receiver_emails = data["emails"]

subject = f"Prices for - {today_date}"

html_content = f"""
<html>
    <body>
        <h2>Vegetable Prices for {today_date}</h2>
        {email_content}
    </body>
</html>
"""

# Connect to the SMTP server and send the email to multiple recipients
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    
    for receiver_email in receiver_emails:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        
        # Attach the HTML content to the email
        message.attach(MIMEText(html_content, "html"))
        
        server.sendmail(sender_email, receiver_email, message.as_string())
        
    print("Emails sent successfully")
except Exception as e:
    print("Error sending emails:", e)
finally:
    server.quit()