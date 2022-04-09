
from PIL import Image, ImageDraw, ImageFont
import requests
import io


def create_dem(photo_url: str, text_big: str, text_small: str) -> int:
    try:
        photo = requests.get(photo_url).content
        photo = Image.open(io.BytesIO(photo))

        arial = ImageFont.truetype('res/fonts/TNR.ttf', 50)
        times = ImageFont.truetype('res/fonts/MRB.ttf', 85)
        dem = Image.open('res/demotivator_pattern.png')

        photo = photo.resize((1199, 928), Image.ANTIALIAS)
        dem.paste(photo, (97, 93))

        draw = ImageDraw.Draw(dem)
        
        w1, h1 = times.getsize(text_big)
        draw.text((700 - (w1 / 2), 1423 - 350), text_big, font=times, fill='white')

        w2, h2 = arial.getsize(text_small)
        draw.text((700 - (w2 / 2), 1423 - 200), text_small, font=arial, fill='white')

        dem.save('res/last_dem.jpg')

        return 0

    except Exception as e:
        print(e)
        return 1
