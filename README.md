<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="FoodGrab_Scrapping" />

  &#xa0;

  <!-- <a href="https://foodgrab_scrapping.netlify.app">Demo</a> -->
</div>

<h1 align="center">FoodGrab_Scrapping</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/paritoshtripathi935/Foodgrab_Scrapping?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/paritoshtripathi935/Foodgrab_Scrapping?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/paritoshtripathi935/Foodgrab_Scrapping?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/paritoshtripathi935/Foodgrab_Scrapping?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/{{YOUR_GITHUB_USERNAME}}/foodgrab_scrapping?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/{{YOUR_GITHUB_USERNAME}}/foodgrab_scrapping?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/{{YOUR_GITHUB_USERNAME}}/foodgrab_scrapping?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  FoodGrab_Scrapping 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-approach">Approach</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

Describe your project

## :sparkles: Approach ##

### Approach - 1
- in devtools if go to the network tab and click on XHR request, so when i click loadmore button [Food Grab](https://food.grab.com/sg/en/restaurants) we can see this request sent to "https://portal.grab.com/foodweb/v2/search"

- so if we go to response section you can see 
```
{"searchResult":{"searchID":"f621f57c6c324a03a9f28eb4231c8395"
```

- get restaurant_id from this response, each restaurant_id stored with id key, then when you click on one restaurants a request sent to https://portal.grab.com/foodweb/v2/merchants/{merchnt_id}

where 2-CYKCVZNZJTDFLE is ‍restaurant_id‍
```
0: {id: "SGDD00739", address: {name: "Lucky Saigon - North Canal Road"},…}
address: {name: "Lucky Saigon - North Canal Road"}
businessType: "FOOD"
chainID: "729_Lucky_Saigon"
chainName: "Lucky Saigon"
estimatedDeliveryFee: {currency: {code: "SGD", symbol: "SGD", exponent: 2}, price: 300, priceDisplay: "S$3.00",…}
estimatedDeliveryTime: 30
id: "SGDD00739"
latlng: {latitude: 1.2862877, longitude: 103.84841596}
```


- you can get latitude and longitude from here, make the https://portal.grab.com/foodweb/v2/search request and https://portal.grab.com/foodweb/v2/merchants/{id} with python, but insure all of the http headers must be same with http headers that in the chrome dev tools

but since use of selenium was requested i tried a diffrent way

### Approach - 2
- So since i have to capture a XHR(XMLHttpRequest) request, i have used selenium wire for this for capturing the XHR request, i have used chrome driver for this.
- Solution Desgin 
```
1. Load the python libraries needed
2. def load_more - Load the food.grab.com page and automatically activate the "Load More" button until the page contains all the restaurants in the Singapore area
3. def capture_post_response - Use driver to make a POST request for the "grab_internal_post_api" and then decode the data and store it in json format in post_data.
4. def get_restaurant_latlng - remove all the extra and keep name and location only, then store it in a list of dictionaries.
```
- Given a base_url, capture all restaurants (based on user's submitted location, e.g., sg) latitude & longitude
by intercepting grab-foods internal POST request. self.grab_internal_post_api is found by manually inspecting all XHR made my grab-foods, using chrome dev tools.

- I think aprroach 1 will be easier but will have to pass recapta test i haven't thoufht about this yet.

- I have taken help for various resources since i have to use selenium wire for this and get data from XHR request which i haven't done yet.

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Selenium](https://pypi.org/project/selenium-wire/)
- [Chromedriver](https://chromedriver.chromium.org/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [python](https://python.org/) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/{{YOUR_GITHUB_USERNAME}}/foodgrab_scrapping

# Access
$ cd foodgrab_scrapping

# Setup virtual environment
$ cd python3 -m venv venv

# Install dependencies
$ pip install -r requirements.txt

# Run the project
$ run XHR.py file 

```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/paritoshtripathi935" target="_blank">Paritosh Tripathi</a>

&#xa0;

<a href="#top">Back to top</a>
