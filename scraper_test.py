#%%
import scraper_2 as chrome_scraper
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


# %%

class TestChromeScraperNavigatingWebsite(unittest.TestCase):
        
    def setUp(self):
        self.venues = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
        self.venues.open_page(self.venues.url)

    def test_links_initally_empty(self):
        self.assertListEqual([], self.venues.links)
        print('Links attribute is empty at the onset of the class')

    # def test_specify_search(self):
    #     self.venues..__specify_search("8")
    #     featured_venue = self.venues.driver.find_element(by=By.XPATH, value='//h2[@class="browse-title"]')
    #     destination = featured_venue.find_element(by=By.XPATH, value='./small').text
    #     self.assertEqual(destination, 'Brittany')
    #     print(f'The driver has correctly filtered the region.')
    
    def test_create_list_of_website_links_per_destination(self):
        links_from_value = self.venues.create_list_of_website_links_per_destination(destination_url = None, destination_value="3")
        url = "https://www.frenchweddingvenues.com/french-wedding-venues?regions=3"
        links_from_url = self.venues.create_list_of_website_links_per_destination(destination_url = url)
        self.assertTrue(set(links_from_url) == set(links_from_value), len(links_from_url) > 0)
        print(f"The driver finds the same venues links whether supplied with a url or property value")

    def test_get_all_destinations_urls(self):
        self.venues.get_all_destinations_urls()
        self.assertEqual(max(self.venues.destinations_indices.keys()), len(self.venues.destinations_indices))
        print(f"All {len(self.venues.destinations_indices)} regions are mapped to their names")

    def test_create_list_of_website_links_all_destinations(self):
        self.venues.get_all_destinations_urls()
        self.venues.create_list_of_website_links_all_destinations()
        all_urls = all(link.startswith('https') for link in self.venues.links)
        self.assertTrue(len(self.venues.links) > 0, all_urls)
        print('The driver has found links of venues, which are all urls.')

    def tearDown(self):
        self.venues.driver.quit()

class TestChromeScraperExtractingInfo(unittest.TestCase):
        
    def setUp(self):
        self.venues = chrome_scraper.Scraper("https://www.frenchweddingvenues.com/french-wedding-venues")
        links = self.venues.create_list_of_website_links_per_destination(destination_url = None, destination_value="8")
        test_venue_url = links[0]
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
