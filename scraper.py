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
        self.driver.get(URL)
        time.sleep(5)

    
    def accept_cookies(self):
        try:
            cookies_button = self.driver.find_element(by=By.XPATH, value='//button[text()=" ACCEPT"]')
            cookies_button.click()
            time.sleep(1)

        except:
            pass

    def scroll_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def specify_search(self, destination="paris"):
        destination_field = Select(self.driver.find_element(by=By.XPATH,value='//select[@name="cbs-region"]'))
        destination_field.select_by_value(destination)
        search_button = self.driver.find_element(by=By.XPATH, value='//a[@id="cbs-form-submit"]' )
        search_button.click()
        
    def get_links(self):
        pass

    def get_price(self):
        pass

    def get_day_capacity(self):
        pass

    def get_sleep_capacity(self):
        pass
    
    def get_caterers_preferences(self):
        pass
    
    def get_distance_from(self):
        pass

    def get_description(self):
        pass

    def get_facility(self):
        pass

    def get_additional_info(self):
        pass


#%%
villas = Scraper("https://chateaubeeselection.com")
villas.accept_cookies()
villas.specify_search()
#%%
driver = webdriver.Chrome() 
URL = "https://chateaubeeselection.com/"
driver.get(URL)
time.sleep(5)

#%%
try:
    cookies_button = driver.find_element(by=By.XPATH, value='//button[text()=" ACCEPT"]')
    cookies_button.click()
    time.sleep(1)

except:
    pass
# %%
select = Select(driver.find_element(by=By.XPATH,value='//select[@name="cbs-region"]'))
select.select_by_value("paris")
search_button = driver.find_element(by=By.XPATH, value='//a[@id="cbs-form-submit"]' )
search_button.click()


# %%
close_button = cite_control.find_element(by=By.XPATH, value='//button[@id="getsitecontrol-close"]')

# %%
driver.find_element(by=By.XPATH, value='//button[@class="getsitecontrol-close"]')
# %%
print(driver.find_element(by=By.XPATH, value='//div[@class="getsitecontrol-container"]'))
# %%<button type="button" class="getsitecontrol-close"></button>
# <div class="getsitecontrol-container"><div class="getsitecontrol-images"><img src="https://m2.getsitecontrol.com/images/43516/c1f53d60b78e5faf8fe9f4983e33b960_212073981.jpg" class="getsitecontrol-image" style="position: absolute !important; object-fit: cover !important; object-position: 50% 50% !important; left: 0px !important; top: 0px !important; width: 100% !important; height: 180px !important;"></div><div class="getsitecontrol-body"><div class="getsitecontrol-content"><h1 class="getsitecontrol-title"><div>Subscribe to our Newsletter !</div></h1><p class="getsitecontrol-description"><div>Our most beautiful destinations, our inspirations, our new villas..</div></p><form novalidate="" class="getsitecontrol-form getsitecontrol-valid getsitecontrol-pristine"><div class="getsitecontrol-fields"><div class="getsitecontrol-field getsitecontrol-text getsitecontrol-first getsitecontrol-with-label getsitecontrol-valid"><label for="Name" class="getsitecontrol-field-title"><div>Name</div></label><input id="Name" class="getsitecontrol-input-text" required="" type="text" name="Name" placeholder="Nom"></div><div class="getsitecontrol-field getsitecontrol-text getsitecontrol-with-label getsitecontrol-valid"><label for="Surname" class="getsitecontrol-field-title"><div>Surname</div></label><input id="Surname" class="getsitecontrol-input-text" required="" type="text" name="Surname" placeholder="Prénom"></div><div class="getsitecontrol-field getsitecontrol-email getsitecontrol-last getsitecontrol-with-label getsitecontrol-valid"><label for="email" class="getsitecontrol-field-title"><div>Email</div></label><input id="email" class="getsitecontrol-input-text" required="" type="email" name="email" placeholder="Email"></div></div><div class="getsitecontrol-buttons"><button type="submit" class="getsitecontrol-button getsitecontrol-primary"><span>I subscribe to the Newsletter</span></button></div></form></div></div><button type="button" class="getsitecontrol-close"></button></div>
# <div class="getsitecontrol-body"><div class="getsitecontrol-content"><h1 class="getsitecontrol-title"><div>Subscribe to our Newsletter !</div></h1><p class="getsitecontrol-description"><div>Our most beautiful destinations, our inspirations, our new villas..</div></p><form novalidate="" class="getsitecontrol-form getsitecontrol-valid getsitecontrol-pristine"><div class="getsitecontrol-fields"><div class="getsitecontrol-field getsitecontrol-text getsitecontrol-first getsitecontrol-with-label getsitecontrol-valid"><label for="Name" class="getsitecontrol-field-title"><div>Name</div></label><input id="Name" class="getsitecontrol-input-text" required="" type="text" name="Name" placeholder="Nom"></div><div class="getsitecontrol-field getsitecontrol-text getsitecontrol-with-label getsitecontrol-valid"><label for="Surname" class="getsitecontrol-field-title"><div>Surname</div></label><input id="Surname" class="getsitecontrol-input-text" required="" type="text" name="Surname" placeholder="Prénom"></div><div class="getsitecontrol-field getsitecontrol-email getsitecontrol-last getsitecontrol-with-label getsitecontrol-valid"><label for="email" class="getsitecontrol-field-title"><div>Email</div></label><input id="email" class="getsitecontrol-input-text" required="" type="email" name="email" placeholder="Email"></div></div><div class="getsitecontrol-buttons"><button type="submit" class="getsitecontrol-button getsitecontrol-primary"><span>I subscribe to the Newsletter</span></button></div></form></div></div>