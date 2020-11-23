from pdf2image import convert_from_path 
  
  
# Store Pdf with convert_from_path function 
images = convert_from_path('/home/agastya/Downloads/timeTables/November23.pdf') 
  
for img in images: 
    img.save('/home/agastya/Downloads/timeTables/November23JPG.jpg', 'JPEG')

from PIL import Image
import PIL.ImageOps    

image = Image.open('/home/agastya/Downloads/timeTables/November23JPG.jpg')

inverted_image = PIL.ImageOps.invert(image)

inverted_image.save('/home/agastya/Downloads/timeTables/November23JPGDARK.jpg')
