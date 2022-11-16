#%%
import time
import os
import os.path
import json
import requests
from selenium import webdriver
from time import sleep, gmtime, strftime
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Scraper:
    '''
    This class scrapes data of the wedding venues presented.

    Attributes:
        url (string): the url of the website
        driver: Selenium webdriver
        links (list): links of all the venues on the website
        data (dict): a dictionary with keys as ids and values as features extracted for each property

    '''
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome() 
        self.links = []
        time.sleep(5)
        self.data = dict()

    
    def accept_cookies(self):
        """ Accept cookies if the button exists."""
        try:
            cookies_button = self.driver.find_element(by=By.XPATH, value='//a[@class="cbc-cookie-notice__button cbc-cookie-notice__button--allow"]')
            cookies_button.click()
            time.sleep(1)

        except:
            pass

    def scroll_page(self):
        """ Scroll a page down."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def open_page(self, link):
        """ Launches a new browser and opens the given link in the browser instance."""
        self.driver.get(link)

    def specify_search(self, destination="Brittany"):
        """ Fill in the destination for the venue and start the search.

        Args:
            destination (str): 

        """
        destination_field = Select(self.driver.find_element(by=By.XPATH,value='//select[@name="regions"]'))
        destination_field.select_by_value("8")
        # time for the search to load
        time.sleep(5)
        search_button = self.driver.find_element(by=By.XPATH, value='//button[@type="submit"]' )
        search_button.click()
        
        
    def create_list_of_website_links(self):
        """ Create a list of all links to the venues presented on the page."""
        # search_results = self.driver.find_element(by=By.XPATH, value='//ul[@class="uk-grid uk-grid-match"]' )
        search_content = self.driver.find_element(by=By.XPATH, value='//div[@id="search-results-list"]')
        ul_tag = search_content.find_element(by=By.XPATH, value='./ul' )
        search_venues = ul_tag.find_elements(by=By.XPATH, value='./li')
    
        for venue in search_venues:
            time.sleep(1)
            a_tag = venue.find_element(by=By.XPATH, value='.//a[@class="major-link"]' )
            self.links.append(a_tag.get_attribute("href"))

    def get_loc_capacity_price_name(self):
        """ Scrap an individual page for a name, location, number of guests, capacity, price."""
        venue_basics = self.driver.find_element(by=By.XPATH, value='//div[@class="venue-basics"]')
        venue_name = venue_basics.find_element(by=By.XPATH, value='.//span')
        items_dict = {'name': venue_name.text}
        venue_items_div = venue_basics.find_element(by=By.XPATH, value='./div')
        venue_items = venue_items_div.find_elements(by=By.XPATH, value='./div')
        items_dict_extend={"location": None, "guests": None, 'sleeps': None, 'from': None }
        for i, item in enumerate(venue_items):
            # print(item.text)
            try:
                items_dict_extend[list(items_dict_extend.keys())[i]] = item.text
            except:
                items_dict_extend[f"misc[{i+1}]"] = item.text
        items_dict.update(items_dict_extend)
        return items_dict

    def get_description(self):
        """ Scrap an individual page for text in the 'Description' part."""
        description_section = self.driver.find_element(by=By.XPATH, value='//section[@id="description"]')
        return description_section.text

    def get_additional_info(self):
        """ Scrap any additional information on the venue under the venue-features"""
        venue_features = self.driver.find_element(by=By.XPATH, value='//section[@class="venue-features"]')
        return venue_features.text
    
    def get_images(self):
        """ Get references for all images depicted on the venue page."""
        images_venue_section = self.driver.find_element(by=By.XPATH, value='//ul[@id="photo-gallery"]')
        images = images_venue_section.find_elements(by=By.XPATH, value='.//img')
        images_list = []
        for image in images:
            images_list.append(image.get_attribute('src'))
        return images_list
    
    @staticmethod
    def create_folder(dirName):
        """ A static method to creare a directory in the project folder."""
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ") 
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")

    @staticmethod
    def save_json_file(dirName, data):
        """ A static method to save a json file."""
        with open(dirName, 'w') as fp:
            json.dump(data, fp, default=lambda o: '<not serializable>')

    @staticmethod
    def download_img(parent_folder, image_url, id):
        """ Downloads an image into a parent folder
        
        Args:
            parent_folder (str): a name of the parent folder for the image
            image_url (str): reference of the image
            id (str): unique id for the image

        """
        img_data = requests.get(image_url).content
        file_path = os.path.join(parent_folder, id, 'images', strftime("%Y%m%d_%H%M%S_", gmtime())+id+'.jpg')
        with open(file_path, 'wb') as handler:
            handler.write(img_data)

    def extract_data(self):
        """ Scrap all venues extracted.

            Extract features for each venue saved in the links attribute using previously defined methods. 
            Save all results in the "raw_data" folder.

        """
        parentDir = 'raw_data'
        Scraper.create_folder(parentDir)
        for link in self.links:
            self.open_page(link)
            id = str(uuid4())
            Scraper.create_folder(dirName=os.path.join(parentDir , id))
            Scraper.create_folder(dirName=os.path.join(parentDir, id, 'images'))
            properties_dict = self.get_loc_capacity_price_name()
            properties_dict['timestamp'] = time.time()
            properties_dict['description'] = self.get_description()
            properties_dict['images'] = self.get_images()
            properties_dict['additional_info'] = self.get_additional_info()
            
            self.data.setdefault(id, properties_dict)
            dirName = os.path.join(parentDir, id, 'data.json')
            Scraper.save_json_file(dirName, data=properties_dict)
            Scraper.download_img(parentDir, self.data[id]['images'][0], id)
        # self.download_img(self, image_url=self.data['images'][0], id=id)
    
    def main_run(self):
        """ Runs the entire website scrapping."""
        self.open_page(self.url)
        self.accept_cookies()
        self.specify_search()
        self.create_list_of_website_links()
        self.extract_data()
          
if __name__ == "__main__":
    wedding = Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
    wedding.main_run()
    


