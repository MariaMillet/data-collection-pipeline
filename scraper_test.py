#%%
import scraper as chrome_scraper
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


# %%

class TestChromeScraperNavigatingWebsite(unittest.TestCase):
        
    def setUp(self):
        self.venues_scraper = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
        self.venues_scraper.open_page(self.venues_scraper.url)

    def test_links_initally_empty(self):
        self.assertListEqual([], self.venues_scraper.links_venues)
        print('Links attribute is empty at the onset of the class')
    
    def test_create_list_of_website_links_per_destination(self):
        links_from_value = self.venues_scraper.create_list_of_website_links_per_destination(destination_url = None, destination_value="3")
        url = "https://www.frenchweddingvenues.com/french-wedding-venues?regions=3"
        links_from_url = self.venues_scraper.create_list_of_website_links_per_destination(destination_url = url)
        self.assertTrue(set(links_from_url) == set(links_from_value), len(links_from_url) > 0)
        print(f"The driver finds the same venues links whether supplied with a url or property value")

    def test_get_all_destinations_urls(self):
        self.venues_scraper.get_all_destinations_urls()
        self.assertEqual(max(self.venues_scraper.destinations_indices.keys()), len(self.venues_scraper.destinations_indices))
        print(f"All {len(self.venues_scraper.destinations_indices)} regions are mapped to their names")

    def test_create_list_of_website_links_all_destinations(self):
        self.venues_scraper.get_all_destinations_urls()
        self.venues_scraper.create_list_of_website_links_all_destinations()
        all_urls = all(link.startswith('https') for link in self.venues_scraper.links_venues)
        self.assertTrue(len(self.venues_scraper.links_venues) > 0, all_urls)
        print('The driver has found links of venues, which are all urls.')

    def tearDown(self):
        self.venues_scraper.driver.quit()

class TestChromeScraperExtractingInfo(unittest.TestCase):
        
    def setUp(self):
        self.venues_scraper = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
        links = self.venues_scraper.create_list_of_website_links_per_destination(destination_url = None, destination_value="8")
        test_venue_url = links[0]
        self.venues_scraper.open_page(test_venue_url)
    
    # def test_get_loc_capacity_price_name(self):
    #     result = self.venues_scraper.get_loc_capacity_price_name()
    #     self.assertIsInstance(result, dict)
    #     print('get_loc_capacity_price_name returns a dictionary')

    def test_get_loc_capacity_price_name(self):
        result = self.venues_scraper.get_loc_capacity_price_name()
  
        non_empty_values = all(bool(result) for result in list(result.values()))
        self.assertTrue(non_empty_values, isinstance(result, dict))
        print('The driver extracts information about the location/capacity/price/name in a dictionary.')

    def test_get_description(self):
        result = self.venues_scraper.get_description()
        self.assertIsInstance(result, str)
        print('The driver extracts a "description" info in a string format.')
    
    def test_get_additional_info(self):
        result = self.venues_scraper.get_additional_info()
        self.assertIsInstance(result, str)
        print('The driver extracts any additional info in a string format.')

    def test_get_images(self):
        result = self.venues_scraper.get_images()
        self.assertTrue(result)
        print('The driver extracts links to images in a string format.')
    
    def tearDown(self):
        self.venues_scraper.driver.quit()

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)

# %%
