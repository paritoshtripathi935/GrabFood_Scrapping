import json
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from seleniumwire.utils import decode as sw_decode


class Driver: 
    def __init__(self, driver_path: str = "/home/paritoshtripathi/PycharmProjects/anakin/chromedriver") -> None:
        self.driver_path = driver_path
        self.browser = None
        self.setup()

    def setup(self): # Setup the browser
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.headless = True
        user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' + 
                      'Chrome/60.0.3112.50 Safari/537.36') # Set the user agent
        chrome_opts.add_argument(f'user-agent={user_agent}') # Add the user agent
        chrome_opts.add_argument('--no-sandbox') # Disable sandbox
        chrome_opts.add_argument("--disable-extensions") # Disable extensions
        chrome_opts.add_argument('--disable-dev-shm-usage') # Disable shared memory

        options = { # Set the options for the browser to use the chrome driver and the options
            'exclude_hosts': [
                'google-analytics.com',
                'analytics.google.com',
                'google.com',
                'facebook.com',
                'stats.g.doubleclick.net',
            ],
        }

        self.browser = webdriver.Chrome(executable_path=self.driver_path,
                                        desired_capabilities=chrome_opts.to_capabilities(),
                                        seleniumwire_options=options)  # Create the browser and open the url in it and wait for the page to load completely

    def tear_down(self):  # Close the browser
        self.browser.quit()


# above is the driver class for the browser and the below is the class for the XHR requests and responses  


class Scraper:  
    """
    Given a base_url, capture all restaurants (based on user's submitted location, e.g., sg) latitude & longitude
    by intercepting grab-foods internal POST request.
    self.grab_internal_post_api is found by manually inspecting all XHR made my grab-foods, using chrome dev tools.
    """

    def __init__(self, driver: Driver, base_url: str = "https://food.grab.com/sg/en/restaurants") -> None:  #  initialize the scraper
        self.driver = driver # initialize the driver
        self.base_url = base_url # initialize the base url
        self.grab_internal_post_api = "https://portal.grab.com/foodweb/v2/search"  # initialize the grab-foods internal post api
        self._init_request() # initialize the request

    def _init_request(self):
        self.driver.browser.get(self.base_url)
        sleep(10)

    def load_more(self):  # clicking load more button to load more restaurants in the list
        del self.driver.browser.requests

        condition = EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "ant-btn ant-btn-block")]')) # load more button is present in the page 
        more_results_button = WebDriverWait(self.driver.browser, 10, poll_frequency=1).until(condition) # wait for the load more button to be present

        print('more_results_button: ', more_results_button, '\n') # print the load more button
        more_results_button.click() # click on the load more button
        sleep(10)

        page_num = 1
        while more_results_button: # while the load more button is present in the page
            try:
                print('page_num: ', page_num)
                more_results_button.click() # click the load more button
                more_results_button = WebDriverWait(self.driver.browser, 10, poll_frequency=1).until(condition) # wait for the load more button to appear
                page_num += 1 # increment the page number
                sleep(10)
            except TimeoutException:
                print("No more LOAD MORE RESULTS button to be clicked!!!\n") # if no more load more button to be clicked, break the loop
                break

    def capture_post_response(self):  # capture the post response from grab-foods
        post_data = []
        for r in self.driver.browser.iter_requests():
            if r.method == 'POST' and r.url == self.grab_internal_post_api:  # capture the post response
                # print(f"r.response.status_code: {r.response.status_code}, r.response.reason: {r.response.reason}")

                data_1 = sw_decode(r.response.body, r.response.headers.get('Content-Encoding', 'identity'))  # decode the response
                data_1 = data_1.decode("utf8") # decode the response

                data = json.loads(data_1) # convert the response to json
                post_data.append(data)
                print(post_data)
        return post_data

    def get_restaurant_latlng(self, post_data):
        d = {}
        for p in post_data: # get the restaurants latlng from the post response and save it in a dictionary
            l = p['searchResult']['searchMerchants']  # list of restaurants
            for rst in l: # for each restaurant
                try:
                    d[rst['chainID']] = {'chainName': rst['chainName'], 'latlng': rst['latlng']}  # chainID is the key for the dictionary
                except Exception as err:
                    d[rst['address']['name']] = {'chainName': rst['address']['name'], 'latlng': rst['latlng']} # address is the key for the dictionary
                    # print(rst)
                    # print(type(err), err)
        return d

    def scrape(self):
        self.load_more()  # load more restaurants in the list
        post_data = self.capture_post_response()  # capture the post response  from grab-foods (list of restaurants)
        restaurants_latlng = self.get_restaurant_latlng(post_data)  # get the restaurants latlng from the post response and save it in a dictionary
        return restaurants_latlng

    def save(self, restaurants_latlng, file: str = 'grab_restaurants_latlng.json'):  # save the dictionary to a json file
        with open(file, 'w') as f:  # save the dictionary to a json file
            json.dump(restaurants_latlng, f, indent=4) # indent=4 is for pretty printing the json file
            


if __name__ == "__main__":
    driver_path = "/home/paritoshtripathi/PycharmProjects/anakin/chromedriver"  # path to the chromedriver
    base_url = "https://food.grab.com/sg/en/restaurants"  # base url of the website
    driver = Driver(driver_path)  # initialize the driver
    scraper = Scraper(driver, base_url)  # initialize the scraper
    restaurants_latlng = scraper.scrape() # scrape the restaurants latlng
    scraper.save(restaurants_latlng)  # save the restaurants latlng to a json file
    driver.tear_down() # tear down the driver
