from PIL import Image, ImageDraw, ImageFont
import json
import textwrap
import os

def create_quote_image(quote, background_path, font_path, output_path, width=1080, height=1080):
    # Open the background image
    background_img = Image.open(background_path)
    
    # Resize and crop the background image to fit 1080x1080
    background_img.thumbnail((width, height))
    background_img = background_img.crop((0, 0, width, height))
    
    # Create a draw object
    draw = ImageDraw.Draw(background_img)
    
    # Specify the font and size
    font_size = 48
    font = ImageFont.truetype(font_path, font_size)
    
    # Wrap text
    wrapped_text = textwrap.fill(quote, width=30)
    
    # Get text size
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate text position (centered)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    
    # Add text to image
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=(255, 255, 255), align="center")
    
    # Save the result
    background_img.save(output_path)

# Load quotes from JSON file
with open('quotes.json', 'r') as file:
    quotes = json.load(file)

# Set paths for background image and font file
background_path = "NextQABG.png"
font_path = "RobotoSlab.ttf"

# Ensure the files exist
if not os.path.exists(background_path):
    raise FileNotFoundError(f"Background image not found: {background_path}")
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

# Process each quote
for i, quote in enumerate(quotes):
    create_quote_image(quote, background_path, font_path, f'quote_image_{i}.png')

print("All images have been created successfully.")