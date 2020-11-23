import os
from os import error
import sys
import requests
from datetime import date
sys.path.append("/home/username/pythonprojects/discord-bot/cogs")
from colors import colors
from pdf2image import convert_from_path
from PIL import Image
import PIL.ImageOps


def withoutO(number):

    if str(number)[0] == '0':
        return str(number)[1:]
    return(str(number))


shortmonths = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'May': 'May', 'June': 'Jun',
               'July': 'Jul', 'August': 'Aug', 'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'Decmber': 'Dec'}
months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
          '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

Month = months[str(date.today()).split('-')[1]]
Date = str(date.today()).split('-')[-1]

hits = ['http://www.sanskritischool.edu.in/News/' + shortmonths[Month] + '%20' + withoutO(str(Date))+'.pdf',
        'http://www.sanskritischool.edu.in/News/' +
        Month + '%20' + str(Date)+'.pdf',
        'http://www.sanskritischool.edu.in/News/' +
        shortmonths[Month].upper() + '%20' + withoutO(str(Date))+'.pdf',
        'http://www.sanskritischool.edu.in/News/' +
        Month.upper() + '%20' + str(Date)+'.pdf'
        ]


Downloaded = False

for file in [f for f in os.listdir('.') if os.path.isfile(f)]:
    if Date in file:
        Downloaded = True
    else:
        if 'py' not in file:
            os.remove(f'{file}')

if not Downloaded:
    pdf = None
    for i in range(len(hits)):
        pdf = requests.get(hits[i])
        try:
            pdf.raise_for_status()
            break
        except requests.exceptions.HTTPError:
            continue

    try:
        pdf.raise_for_status()
        with open(f'cogs/{Month}{Date}.pdf', 'wb') as f:
            for chunk in pdf.iter_content(100):
                f.write(chunk)
        print(f'{colors.OKGREEN}DOWNLOADED SCHEDULE WITHOUT ERROR{colors.ENDC}')
    except requests.exceptions.HTTPError:
        print(f'{colors.ERROR}DOWNLOAD SCHEDULE FAILED{colors.ENDC}')
else:
    print(f'{colors.OKGREEN}SCHEDULE ALREADY DOWNLOADED {colors.ENDC}')

images = convert_from_path(f'cogs/{Month}{Date}.pdf')

for img in images:
    img.save(f'cogs/{Month}{Date}.jpg', 'JPEG')

image = Image.open(f'cogs/{Month}{Date}.jpg')

inverted_image = PIL.ImageOps.invert(image)
os.remove(f'cogs/{Month}{Date}.pdf')
os.remove(f'cogs/{Month}{Date}.jpg')

inverted_image.save(f'cogs/{Month}{Date}.jpg')

