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

# Scrape the fuel prices table
fuel_url = "https://dhirajraut27.com.np/fuel-prices"
response = requests.get(fuel_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='fuel-price')
    if table:
        rows = table.find_all('tr')
        
        # Append the fuel prices table to the email content
        email_content = "<h2 class= 'text-center' >Fuel Prices</h2><table class='table table-striped'><tr><th>Fuel Type</th><th>Price</th></tr>"
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            email_content += "<tr>" + "".join(f"<td>{data}</td>" for data in row_data) + "</tr>"
        email_content += "</table><br>"
    else:
        print("Table 'fuel-table' not found.")
else:
    print("Failed to retrieve the webpage.")

# Scrape the prices table
url = "https://ramropatro.com/vegetable"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='commodityDailyPrice')
    if table:
        rows = table.find_all('tr')
        
        # Compose the email content as an HTML table
        email_content += "<h2 class= 'text-center' >Vegetable Prices</h2><table class='table table-striped' ><tr><th>Commodity</th><th>Unit</th><th>Minimum</th><th>Maximum</th><th>Average</th></tr><tr>"
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            email_content += "<tr>" + "".join(f"<td>{data}</td>" for data in row_data) + "</tr>"
        email_content += "</table>"
    else:
        print("Table 'commodityDailyPrice' not found.")
else:
    print("Failed to retrieve the webpage.")

# # Scrape the fuel prices table
# fuel_url = "https://dhirajraut27.com.np/fuel-prices"
# response = requests.get(fuel_url)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     table = soup.find('table', id='fuel-price')
#     if table:
#         rows = table.find_all('tr')
        
#         # Append the fuel prices table to the email content
#         email_content += "<h2>Fuel Prices</h2><table style='border-collapse: collapse; width: 100%; border: 1px solid black;'><tr><th>Fuel Type</th><th>Price</th></tr>"
#         for row in rows:
#             cells = row.find_all('td')
#             row_data = [cell.get_text(strip=True) for cell in cells]
#             email_content += "<tr>" + "".join(f"<td>{data}</td>" for data in row_data) + "</tr>"
#         email_content += "</table>"
#     else:
#         print("Table 'yTable' not found.")
# else:
#     print("Failed to retrieve the webpage.")

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
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Prices Nepal</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    </head>
    <body>
        <img src="https://raw.githubusercontent.com/dhirajraut1/daily-prices-email/main/priceNepalLogo.png" class="img-fluid img-thumbnail rounded mx-auto d-block" width="80px" alt="Price Nepal Logo">
        <h2>Prices for {today_date}</h2>
        {email_content}

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
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
