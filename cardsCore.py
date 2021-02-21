from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from urllib.request import urlopen
import io

import requests


def pullImages(characters):

    image1 = Image.open(requests.get(
        characters[0]['image'], stream=True).raw)
    image2 = Image.open(requests.get(
        characters[1]['image'], stream=True).raw)
    image3 = Image.open(requests.get(
        characters[2]['image'], stream=True).raw)
    card = Image.open('images/card.png')

    image1 = image1.resize((153, 182))
    image2 = image2.resize((153, 182))
    image3 = image3.resize((153, 182))
    card = card.resize((200, 350))

    card_size = card.size

    new_image = Image.new('RGB', (650, card_size[1]), (0x2C2F33))
    new_image.paste(card, (0, 0))
    new_image.paste(card, (card_size[0] + 25, 0))
    new_image.paste(card, ((2*card_size[0]) + 50, 0))

    new_image.paste(image1, (23, 64))
    new_image.paste(image2, (card_size[0] + 23 + 25, 64))
    new_image.paste(image3, ((2*card_size[0]) + 23 + 50, 64))

    draw = ImageDraw.Draw(new_image)

    font = ImageFont.truetype("font.ttf", 18)
    draw.text((23, 15), str(characters[0]['firstName']), (0, 0, 0), font=font)
    draw.text((card_size[0] + 23 + 25, 15), str(characters[1]['firstName']), (0, 0, 0), font=font)
    draw.text(((2*card_size[0]) + 23 + 50, 15), str(characters[2]['firstName']), (0, 0, 0), font=font)

    imageBytes = io.BytesIO()
    new_image.save(imageBytes, format='PNG')
    imageBytes.seek(0)

    return imageBytes
