#%%
from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Scraper:

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome() 
        self.driver.get(self.url)
        self.links = []
        time.sleep(5)

    
    def accept_cookies(self):
        try:
            cookies_button = self.driver.find_element(by=By.XPATH, value='//a[@class="cbc-cookie-notice__button cbc-cookie-notice__button--allow"]')
            cookies_button.click()
            time.sleep(1)

        except:
            pass

    def scroll_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def specify_search(self, destination="Brittany"):
        destination_field = Select(self.driver.find_element(by=By.XPATH,value='//select[@name="regions"]'))
        destination_field.select_by_value("8")
        # time for the search to load
        time.sleep(5)
        search_button = self.driver.find_element(by=By.XPATH, value='//button[@type="submit"]' )
        search_button.click()
        
        
    def get_links(self):
        # search_results = self.driver.find_element(by=By.XPATH, value='//ul[@class="uk-grid uk-grid-match"]' )
        search_content = self.driver.find_element(by=By.XPATH, value='//div[@id="search-results-list"]')
        ul_tag = search_content.find_element(by=By.XPATH, value='./ul' )
        search_venues = ul_tag.find_elements(by=By.XPATH, value='./li')
    
        for venue in search_venues:
            time.sleep(1)
            a_tag = venue.find_element(by=By.XPATH, value='.//a[@class="major-link"]' )
            self.links.append(a_tag.get_attribute("href"))

    def get_loc_capacity_price_name(self):
        venue_basics = self.driver.find_element(by=By.XPATH, value='//div[@class="venue-basics"]')
        venue_items = venue_basics.find_elements(by=By.XPATH, value='./div')
        items=[]
        for item in venue_items:
            items.append(item.text)
        # print(items)

    def get_description(self):
        description_section = self.driver.find_element(by=By.XPATH, value='//section[@id="description"]')
        # print(description_section.text)

    def get_additional_info(self):
        venue_features = self.driver.find_element(by=By.XPATH, value='//section[@class="venue-features"]')
        # print(venue_features.text)
    
    def get_images(self):
        images_venue_section = self.driver.find_element(by=By.XPATH, value='//ul[@id="photo-gallery"]')
        images = images_venue_section.find_elements(by=By.XPATH, value='.//img')
        images_list = []
        for image in images:
            images_list.append(image.get_attribute('src'))
        print(images_list)


    def open_venue_page(self, link):
        self.driver.get(link)
    
    def extract_data(self):
        for link in self.links:
            self.open_venue_page(link)
            self.get_description()
            self.get_loc_capacity_price_name()
            self.get_additional_info()
            self.get_images()

if __name__ == "__main__":
    wedding = Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
    wedding.accept_cookies()
    wedding.specify_search()
    wedding.get_links()
    wedding.extract_data()

