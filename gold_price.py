# import requests
# from bs4 import BeautifulSoup

# url = "https://www.fenegosida.org/rate-history.php"

# response = requests.get(url)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, 'html.parser')
#     header_rate_div = soup.find('div', id='header-rate')
    
#     if header_rate_div:
#         p_tags = header_rate_div.find_all('p')
        
#         if p_tags:
#             email_content = "<h2>Gold/Silver Rate</h2><table><tr><th>Item</th><th>Rate</th></tr>"
#             for p_tag in p_tags:
#                 p_value = p_tag.get_text(strip=True)
#                 start_index = p_value.find('per')
#                 end_index = p_value.find('grm') + 3
#                 item = p_value[:start_index].strip()
#                 value = p_value[end_index:].strip()
#                 email_content += f"<tr><td>{item}</td><td>{value}</td></tr>"
#             email_content += "</table>"
#         else:
#             email_content = "No <p> tags found inside header-rate div."
#     else:
#         email_content = "header-rate div not found."
# else:
#     email_content = "Failed to retrieve the webpage."

# # Add the email_content to the existing email_content
# email_content += "<br>"  # Add a line break before adding more content

# # Now you can add this email_content to your email message


# print(email_content)

import requests
from bs4 import BeautifulSoup

url = "https://www.fenegosida.org/rate-history.php"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    header_rate_divs = soup.find_all('div', id='header-rate')
    
    if len(header_rate_divs) >= 2:
        header_rate_div = header_rate_divs[1]  # Select the second occurrence of the div with id 'header-rate'
        
        p_tags = header_rate_div.find_all('p')
        
        if p_tags:
            email_content = "<h2>Header Rate Values</h2><table border='1'><tr><th>Item</th><th>Value</th></tr>"
            for p_tag in p_tags:
                p_value = p_tag.get_text(strip=True)
                start_index = p_value.find('per')
                end_index = p_value.find('tola')
                item = p_value[:start_index].strip()
                value = p_value[end_index+4:].strip()  # Skip 'grm' and the following space
                email_content += f"<tr><td>{item}</td><td>{value}</td></tr>"
            email_content += "</table>"
        else:
            email_content = "No <p> tags found inside the second header-rate div."
    else:
        email_content = "Second header-rate div not found."
else:
    email_content = "Failed to retrieve the webpage."

# Add the email_content to the existing email_content
email_content += "<br>"  # Add a line break before adding more content

# Now you can add this email_content to your email message

print(email_content)
