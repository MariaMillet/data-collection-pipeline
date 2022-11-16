#%%
import scraper_2 as chrome_scraper
import unittest
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

# venues = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")

# %%

# venues = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
# venues.open_page(venues.url)
class TestChromeScraperNavigatingWebsite(unittest.TestCase):
        
    def setUp(self):
        self.venues = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
        self.venues.open_page(self.venues.url)



    def test_links_initally_empty(self):
        self.assertListEqual([], self.venues.links)
        print('Links attribute is empty at the onset of the class')

    def test_specify_search(self):
        self.venues.specify_search()
        featured_venue = self.venues.driver.find_element(by=By.XPATH, value='//h2[@class="browse-title"]')
        destination = featured_venue.find_element(by=By.XPATH, value='./small').text
        self.assertEqual(destination, 'Brittany')
        print(f'The driver has correctly filtered the region.')
    
    def test_create_list_of_website_links(self):
        self.venues.specify_search()
        self.venues.create_list_of_website_links()
        all_urls = all(link.startswith('https') for link in self.venues.links)
        self.assertTrue(len(self.venues.links) > 0, all_urls)
        print('The driver has found some links, which are all urls.')

    def tearDown(self):
        self.venues.driver.quit()

class TestChromeScraperExtractingInfo(unittest.TestCase):
        

    def setUp(self):
        self.venues = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
        self.venues.open_page(self.venues.url)
        self.venues.specify_search()
        self.venues.create_list_of_website_links()
        test_venue_url = self.venues.links[0]
        self.venues.open_page(test_venue_url)
    
    def test_get_loc_capacity_price_name(self):
        result = self.venues.get_loc_capacity_price_name()
        self.assertIsInstance(result, dict)
        print('get_loc_capacity_price_name returns a dictionary')

    def test_get_loc_capacity_price_name(self):
        result = self.venues.get_loc_capacity_price_name()
  
        non_empty_values = all(bool(result) for result in list(result.values()))
        self.assertTrue(non_empty_values)
        print('The driver extracts information about the location/capacity/price/name')

    def test_get_description(self):
        result = self.venues.get_description()
        self.assertIsInstance(result, str)
        print('The driver extracts a "description" info in a string format.')
    
    def test_get_additional_info(self):
        result = self.venues.get_additional_info()
        self.assertIsInstance(result, str)
        print('The driver extracts any additional info in a string format.')

    def test_get_images(self):
        result = self.venues.get_images()
        self.assertTrue(result)
        print('The driver extracts links to images in a string format.')
    
    def tearDown(self):
        self.venues.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
# %%

mydict = {"key" : "value", "emptykey" : []}
print (bool(mydict["key"]))

print (bool(mydict["emptykey"]))

# %%
