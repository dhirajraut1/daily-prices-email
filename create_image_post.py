import os
import asyncio
import requests
import datetime
from pyppeteer import launch
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')
page_id = os.getenv('PAGE_ID')
base_url = f'https://graph.facebook.com/{page_id}/photos'
fuel_website = "https://dhirajraut27.com.np/fuel-prices/"

# Function to capture screenshot
async def capture_screenshot():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(fuel_website)

    element = await page.querySelector('#fuel-price-img')
    bounding_box = await element.boundingBox()

    await page.screenshot({
        'path': 'fuel-img.png',
        'clip': {
            'x': bounding_box['x'],
            'y': bounding_box['y'],
            'width': bounding_box['width'],
            'height': bounding_box['height']
        }
        })
    await browser.close()

# Capture screenshot
asyncio.get_event_loop().run_until_complete(capture_screenshot())

current_date = datetime.datetime.now().strftime('%Y-%m-%d')
message = f'Fuel Price for {current_date}'
image_path = 'example1.png'
# image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fuel.png')


# Create a file object
with open(image_path, 'rb') as image_file:
    # Parameters for the post
    params = {
        'access_token': access_token,
        'message': message,
    }
    
    # Create a dictionary for files
    files = {'source': image_file}
    
    # Make a POST request to create the post
    response = requests.post(base_url, data=params, files=files)

# Check if the request was successful
if response.status_code == 200:
    print("Post created successfully!")
else:
    print("Error:", response)
