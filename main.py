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
        email_content = "<h2>Fuel Prices</h2><table id='fuel'><tr><th>Fuel Type</th><th>Price</th></tr>"
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            email_content += "<tr>" + "".join(f"<td>{data}</td>" for data in row_data) + "</tr>"
        email_content += "</table><br>"
    else:
        print("Table 'fuel-table' not found.")
else:
    print("Failed to retrieve the webpage.")

# Scrape gold prices
gold_url = "https://www.fenegosida.org/rate-history.php"

response = requests.get(gold_url)
email_content += "<h2>Gold/Silver Rate</h2><table id='gold'><tr><th>Item</th><th>Rate</th></tr>"


if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    header_rate_div = soup.find('div', id='header-rate')
    
    if header_rate_div:
        p_tags = header_rate_div.find_all('p')
        
        if p_tags:
            for p_tag in p_tags:
                p_value = p_tag.get_text(strip=True)
                start_index = p_value.find('per')
                end_index = p_value.find('grm') + 3
                item = p_value[:start_index].strip()
                value = p_value[end_index:].strip()
                email_content += f"<tr><td>{item}</td><td>{value}</td></tr>"
            email_content += "</table>"
        else:
            email_content += "No <p> tags found inside header-rate div."
    else:
        email_content += "header-rate div not found."
else:
    email_content += "Failed to retrieve the webpage."

# Scrape the prices table
url = "https://kalimatimarket.gov.np/lang/en"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='commodityDailyPrice')
    if table:
        rows = table.find_all('tr')
        
        # Compose the email content as an HTML table
        email_content += "<h2>Vegetable Prices</h2><table id='vegetable'><tr><th>Commodity</th><th>Minimum</th><th>Maximum</th><th>Average</th></tr><tr>"
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            email_content += "<tr>" + "".join(f"<td>{data}</td>" for data in row_data) + "</tr>"
        email_content += "</table>"
    else:
        print("Table 'commodityDailyPrice' not found.")
else:
    print("Failed to retrieve the webpage.")

# Add the email_content to the existing email_content
email_content += "<br>" 

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
        <style>
        table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        #gold th {{
            background-color: #ffd700;
        }}
        
        #fuel th {{
            background-color: #00c4ff;
        }}
        
        #vegetable th {{
            background-color: #32cd32;
        }}

        tr:nth-child(even) {{
            background-color: #f2f8ff;
        }}
        .parent {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
    </style>
    </head>
    
    <body>
        <div class="parent">
            <img src="https://raw.githubusercontent.com/dhirajraut1/daily-prices-email/main/priceNepalLogo.png" class="main-logo" width="80px" alt="Price Nepal Logo">
        </div>
        <h2>Prices for {today_date}</h2>
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
