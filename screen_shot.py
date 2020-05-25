from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pytesseract
from PIL import Image
import pyscreenshot as ImageGrab
from log import email, password


# Method to screen shot the 6-digit SMS code Amazon sends to verify the user
# Not sure if it should be global function, I'd appreciate feedback on this! :)
def screen_shot():
    # Desktop coordinate of the iMessage you receive from Amazon
    image = ImageGrab.grab(bbox=(1128, 68, 1240, 82))
    image.save('code5.png')

    # Using our OCR
    im = Image.open('code5.png')
    text = pytesseract.image_to_string(im, lang="eng")
    print(text)

    write_file = open("output1.txt", "w")
    write_file.write(text)
    write_file.close()

    # Extracting the code from the screen shot
    screen = open("output1.txt", "r")
    output = screen.readline()
    output2 = output.split()
    code = output2[0]
    return code


print(screen_shot())
