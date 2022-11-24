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
from selenium.webdriver.chrome.options import Options

class Scraper:
    '''
    This class scrapes data across regions in France, which feature wedding venues.

    Attributes:
        url (string): the url of the website
        driver: Selenium webdriver
        links_venues (list): venues' links
        links_to_destinations (list): links to regions where venues are located
        data (dict): a dictionary with keys as ids and values as features extracted for each property
        destinations_indices (dict): mapping from the index of the region (as depicted on the website) to the region name and its url

    '''
    def __init__(self, url):
        self.url = url
        options = Options()
        options.headless = True
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')  
        self.driver = webdriver.Chrome(options=options) 
        self.links_venues = []
        self.links_to_destinations = []
        self.data = dict()
        self.destinations_indices = dict()

    
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

    def __specify_search(self, destination_value="8"):
        """ Fill in the destination value for the venue and start the search.

        The function may be used in case the format of the links to the destinations is amended by a website. 
        In such a case the user will still be able to navigate to a specific destination by selecting Regions
        and clicking a "Submit" button.

        Args:
            destination (str): an index of the region (1 to 13) in a string format

        """
        self.open_page(self.url)
        destination_field = Select(self.driver.find_element(by=By.XPATH,value='//select[@name="regions"]'))
        destination_field.select_by_value(destination_value)
        # time for the search to load
        time.sleep(5)
        search_button = self.driver.find_element(by=By.XPATH, value='//button[@type="submit"]' )
        search_button.click()
        
    def get_all_destinations_urls(self):
        """ Extracts names and indices values of elements corresponding to regions.

        Populates destination_indices with integer index values as keys and a name and a url as values. 

        """
        
        self.open_page(self.url)
        self.accept_cookies()
        destinations = self.driver.find_elements(by=By.XPATH, value='//select[@name="regions"]/option')  
        for destination in destinations:
            destination_index = destination.get_attribute('value')
            destination_name = destination.text
            if destination_index:
                try:
                    url = self.url + '?regions=' + str(destination_index)
                    self.destinations_indices[int(destination_index)] = {'name': destination_name, 'url': url}
                except:
                    pass


    def create_list_of_website_links_per_destination(self, destination_url=None, destination_value = "8"):
        """ Create a list of all links to the venues presented on the page.

        If the url is supplied then the respective page will be loaded and "destination_value" ignored.
        If the url is not supplied than the page corresponding to the index of the region will be loaded from the 
        "Search" panel of the main website.
        This multi functionality is useful in case one or the other method of page loading stops working.
        
        Args:
            destination_url (str): a url of the webpage corresponding to a certain region
            destination_value (str): an index of the region (1 to 13) in a string format
        
        Returns:
            links_per_destination (lst): a list of extracted venues

        """
        links_per_destination = []
        if destination_url:
            self.open_page(destination_url)
        else:
            self.__specify_search(destination_value)
        time.sleep(2)
        search_content = self.driver.find_element(by=By.XPATH, value='//div[@id="search-results-list"]')
        ul_tag = search_content.find_element(by=By.XPATH, value='./ul' )
        search_venues = ul_tag.find_elements(by=By.XPATH, value='./li')
    
        for venue in search_venues:
            time.sleep(1)
            a_tag = venue.find_element(by=By.XPATH, value='.//a[@class="major-link"]' )
            links_per_destination.append(a_tag.get_attribute("href"))

        return links_per_destination

    def create_list_of_website_links_all_destinations(self):
        """ Loops through all possible regions and extracts links to venues. 
            
            Links_venues attribute of the class is populated.

        """
        for prop_dict in self.destinations_indices.values():
            try:
                extracted_links_per_destination = self.create_list_of_website_links_per_destination(prop_dict['url'])
                self.links_venues.extend(extracted_links_per_destination)
                print(f"Properties links found for destination {prop_dict['name']}")
            except:
                print(f"No proprties links found for destination {prop_dict['name']}")


    def get_loc_capacity_price_name(self):
        """ Scrap an individual page for a name, location, number of guests, capacity, price.
            Assumes that the currently loaded page is that of a particular venue.

            Returns:
                items_dict (dict): "location / guests / sleeps / from" values are populated as well as 
                                    any further "misc" items

        """
        venue_basics = self.driver.find_element(by=By.XPATH, value='//div[@class="venue-basics"]')
        venue_name = venue_basics.find_element(by=By.XPATH, value='.//span')
        items_dict = {'name': venue_name.text}
        venue_items_div = venue_basics.find_element(by=By.XPATH, value='./div')
        venue_items = venue_items_div.find_elements(by=By.XPATH, value='./div')
        items_dict_extend={"location": None, "guests": None, 'sleeps': None, 'from': None }
        for i, item in enumerate(venue_items):
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
        """ Get references in a list format for all images depicted on the venue page."""
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
        """ Scraps information for all venues.

            Extract features for each venue saved in the links_venues attribute using previously defined methods. 
            Save all results in the "raw_data" folder.

        """
        parentDir = 'raw_data'
        Scraper.create_folder(parentDir)
        for link in self.links_venues:
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
        self.get_all_destinations_urls()
        self.create_list_of_website_links_all_destinations()
        self.extract_data()
        self.driver.quit()
          
if __name__ == "__main__":
    wedding = Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
    wedding.main_run()
    # wedding.get_all_destinations_urls()
    # wedding.create_list_of_website_links_all_destinations()
    
    # wedding.create_list_of_website_links_all_destinations()

    # wedding.create_list_of_website_links_per_destination("https://www.frenchweddingvenues.com/french-wedding-venues?regions=3")
    # wedding.open_page("https://www.frenchweddingvenues.com/french-wedding-venues?regions=3")
    # print(type(wedding.destinations_indices[3]['url']))
    # wedding.open_page(wedding.destinations_indices[3]['url'])
    



    # %%
int("3")
# %%
