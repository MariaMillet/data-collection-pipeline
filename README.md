# Data Collection Pipeline
This scraper is intended to collect data from a wedding venues website "https://www.frenchweddingvenues.com/french-wedding-venues". The scraper file is `scraper_2.py`.

## 


## Unit Testing
* Unit tests were implemented in the `scraper_test.py` file to test that all public functions are working as expected. 
* Tests were spread across 2 classes - both inherit from `unittest.TestCase` class. The tests were split because of different `setUp()` methods used.
* `TestChromeScraperNavigatingWebsite` tested for the following:
    * `links_venues` attribute is initially an empty list
    * `create_list_of_website_links_per_destination` tests that the method works both when supplied with the url or region number. Here, region "3" was used as an example.
    * `get_all_destinations_urls` checks that links to all available regions are found by comparing the length of a list with regions links to the region with the highest number - i.e. making sure that links to all 13 regions are found.
    * `test_create_list_of_website_links_all_destinations` tests that the mathod that iterates through all regions links and scraps all of the respective venues works correctly.

* `TestChromeScraperExtractingInfo` tested that the Scraper extracts necessary information, using the first venue link found for the region = "8"/"Britanny" as a test example.:
    * `test_get_loc_capacity_price_name` tests that the method          `get_loc_capacity_price_name` returns a non-empty dictionary instance, i.e. results for loc/capacity/price etc are found. 

    * `test_get_description` tests that the driver extracts a "description" info in a string format.
    
    * `test_get_additional_info` tests that the driver extracts any "additional info" into a string format.

    * `test_get_images` tests that the driver extracts links to images in a string format.

## Containerising the scraper
* `Dockerfile` creates an image `venues` by:
    * pulling a python image 
    * adding and installing Google Chrome and Chrome driver.
    * copying scraper into a Docker image
    * installing requirements by running `requirements.txt` file
    * running the `scraper_2.py` file 
* `docker-compose.yml` creates and starts a container.
    * a mounted `volume` `scrapped_data` is added to share scrapped data between a container and a local machine.
    * the scrapped data is stored locally in the folder "$PWD"/data_from_container
    * using a `docker compose up` command lets us avoid having to retype docker run -v "$PWD"/data_from_container:/raw_data -it -d venues.

## CI/CD pipeline
* Set up the relevant GitHub secrets that contain the credentials required to push to the Dockerhub:
    * First secret: create a `DOCKER_HUB_USERNAME` and your Docker ID as value
    * Create a new Personal Access Token for Docker Hub.
    * Second secret: add the PAT as a second secret with the name `DOCKER_HUB_ACCESS_TOKEN`
* The workflow and its steps are defined in the `.github/workflows/main.yml`
    * The workflow runs on every push event for the main branch
    * The job is to sign in to Docker Hub, build and push a Docker image.
