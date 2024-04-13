import os
import asyncio
import requests
import datetime
import nepali_datetime
from pyppeteer import launch
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')
page_id = os.getenv('PAGE_ID')
base_url = f'https://graph.facebook.com/{page_id}/photos'
fuel_website = "https://dhirajraut27.com.np/fuel-prices/"
gold_website = "https://www.fenegosida.org/rate-history.php"
fuel_website_element = "#fuel-price-img"
gold_website_element = ".rate-content"

# Function to capture screenshot
async def capture_screenshot(url, element_id, filename):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})
    await page.goto(url)

    element = await page.querySelector(element_id)
    bounding_box = await element.boundingBox()

    await page.screenshot({
        'path': f'{filename}.png',
        'clip': {
            'x': bounding_box['x'],
            'y': bounding_box['y'],
            'width': bounding_box['width'],
            'height': bounding_box['height']
        }
        })
    await browser.close()

# Capture screenshot
asyncio.get_event_loop().run_until_complete(capture_screenshot(fuel_website,fuel_website_element, 'fuel'))
asyncio.get_event_loop().run_until_complete(capture_screenshot(gold_website,gold_website_element, 'gold'))

# current_date = datetime.datetime.now().strftime('%Y-%m-%d')
nepali_date = nepali_datetime.date.today()
message = f'Price for {nepali_date}'
image_paths = ['fuel.png', 'gold.png']
# image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fuel.png')


for image_path in image_paths:
# Create a file object
    try:
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
    except Exception as e:
        print(f"Error uploading image {image_path}: {e}")
