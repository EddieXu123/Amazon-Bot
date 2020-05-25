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


class AmazonBot:
    def __init__(self):
        # Create a browser we can play on
        self.driver = webdriver.Chrome()

    def log_on(self):
        """First, we must log into our Amazon account"""
        # Go to Amazon
        self.driver.get('https://amazon.com')
        sleep(2)
        # Log in
        self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/div[2]/div/a[2]/span[1]').click()
        # Enter email
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/form/div/div/div/div[1]/input[1]').send_keys(email)
        # Continue
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/form/div/div/div/div[2]/span/span/input').click()
        # Click keep me signed in
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div/form/div/div[2]/div/div/label/div/label/input').click()
        # Enter password
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div/form/div/div[1]/input').send_keys(password + Keys.RETURN)
        sleep(2)
        # Authentication will be required, click continue
        self.driver.find_element_by_id('continue').click()
        # Amazon will send you an SMS to verify you are the one using the account
        sleep(6)  # Wait a bit for the message to appear on your computer screen
        # Use the OCR to get the 6-digit Auth code and continue onto your account
        self.driver.find_element_by_class_name('a-input-text').send_keys(screen_shot() + Keys.RETURN)

        # Now I have logged onto my Amazon account
        sleep(2)

    # This method buys all the stuff
    def purchase(self):
        items = ["ramen x2 spicy", "sweet spicy chili doritos", "guitar capo"]  # Replace this with whatever you want to buy
        for i in range(0, len(items)):  # The for loop that does your shopping
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/header/div/div[1]/div[3]/div/form/div[3]/div[1]/input').send_keys(
                items[i] + Keys.RETURN)
            sleep(2)  # Wait for items to load
            # Array holding the items/products on the page
            products = self.driver.find_elements_by_class_name('sg-col-inner')
            # The first (normally featured) option is the 6th 'product' in the list
            products[5].click()
            sleep(3)  # Wait for product page to load
            # Now, I am on the page of the featured item you want to buy

            # Sometimes when you order something that is sponsored, you may be asked to choose to a monthly subscription.
            # When this happens, there will also be an option that appears for you to select a 'One-time purchase'.
            # To select this option, simply go to the one-time-purchase. Because we do not know when this subscription option
            # will pop up, we must use a Finite State Machine to first check if this button appears, and if it doesn't just add to cart straightaway
            try:
                # If we are given the option to choose a one-time subscription, select that option
                self.driver.find_element_by_class_name('a-icon-radio-inactive').click()
                sleep(1)
                # Add to cart
                self.driver.find_element_by_id('add-to-cart-button').click()
            except NoSuchElementException:  # If we are not given the option to choose the one-time subscription
                # just add to car straightaway
                self.driver.find_element_by_id('add-to-cart-button').click()
            sleep(1)
            self.driver.get('https://amazon.com')  # Go back to the main page to buy more stuff

        sleep(2)
        # Once we have our cart filled out, we can check out

    def check_out(self):
        # Select your shopping cart
        self.driver.find_element_by_id('nav-cart-count').click()
        sleep(2)
        # Proceed to checkout
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[4]/div[1]/div[5]/div/div[1]/div[2]/form/div/div/div/span/span/input').click()

        """You will be prompted with shipping options. Sometimes, the default option is the most expensive one
        I want to select the cheapest one because I am broke, and I also do not want to select Amazon Prime student
        because I will forget to cancel it in a week and then get charged for 2 consecutive years like I have since 2018.
        To select the Free Shipping options with no Prime Student bind, choose the first button to the right of each product"""

        # Variable to keep track of the items that you are buying (separated by different shipping dates)
        group = self.driver.find_elements_by_class_name('shipment')
        # We want to click on the the first 'radio-standard' button in our group
        for item_group in range(0, len(group)):
            # Click the free shipping without needing to be Amazon Prime Student in each item-group
            group[item_group].find_element_by_class_name('radio-standard').click()
            sleep(3)
            # The interface will reload so we need to re-assign group
            group = self.driver.find_elements_by_class_name('shipment')

        # Now, we have selected the cheapest options and can place our order
        self.driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/form/div/div/div/div[2]/div[2]/div/div[1]/span/span/input').click()


# Call the self
bot = AmazonBot()
bot.log_on()
bot.purchase()
bot.check_out()
