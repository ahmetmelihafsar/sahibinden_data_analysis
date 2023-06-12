# Sahibinden Data Analysis

## Introduction

This project is a data analysis project for Sahibinden.com. The project is written in Python. The aim of this project is to scrape car listings data from sahibinden.com and to produce some insight into the data. The information that came from the listings is also being used to train prediction models.

## Table of Contents

- [Sahibinden Data Analysis](#sahibinden-data-analysis)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Scraping Story](#scraping-story)
    - [Browser](#browser)
    - [Pagination](#pagination)
    - [Captcha](#captcha)
    - [Others](#others)

## Installation

The project is written in Python 3.11, but it should work fine for Python 3.9+. The required packages are listed in the requirements.txt file. To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

The project is divided into two parts: scraping and analysis. The scraping part is done by the [`scraper.ipynb`](./scraper.ipynb) file. The analysis part is done by the [`data_science.ipynb`](./data_science.ipynb) file. [`helpers.py`](./helpers.py) has some free functions for dissecting the listing row and it also has the hardcoded brand IDs for the URL query.  

You can access the listing data I retrieved via "./data" folder, and "./raw_data" folder contains some samples I used when writing BeautifulSoup expressions.  

## Scraping Story

### Browser

For scraping, I decided that if I could use `requests` library and get every page, it would be very easy. However, I saw that the search URL actually does not return html site with the `<table>` item. The javascript code of the site injects the data after the webpage is loaded, so I had to use a full browser in order to properly load the page. The browser is controlled by `selenium`.  


### Pagination

I examined "sahibinden.com" and saw that search pages pagination is done by `&pagingSize=` and `&pagingOffset=` URL parameters. I saw that maximum number for `pagingSize` is 50. After that, I started to run the full loop for every page. After the data is retrieved and I started working on the data analysis part, I realized that there were a huge amount of duplicate entries in my data. After a quick investigation, I realized that "sahibinden.com" does not show any new listings after page 20, and it shows only the listings in the 20th page repeatedly.

The solution I found to this issue was to use car brands as a secondary search parameter in order to decrease maximum number of listings per search query, and concatenate the each brand list into one. That way all listings could be received, given that no car brand has more than 50*20=1000 listings currently active. That seems like a reasonable assumption, even though there were a few that was over the 1000 listing mark.

### Captcha

Because I was using vanilla selenium, the website was not letting my program browse it and presenting a CloudFlare captcha. It is the first line of defense aganist script kiddies (like me LOL), so I had to step up. At first, I tried to install `Privacy Pass` extension to Chrome. This extension is provided by Cloudflare itself, and it aims to reduce the number of interactions that require a captcha check by storing a solved identifier and giving you a pass for a specified period of time. That way you do not need to fill out captchas excessively, however this process did not help and I still could not pass a captcha even though I myself personally solved the captcha. This led me to a deeper research and where I tried different possible solutions, and after a while I came across `undetected_chromedriver` which was right up my alley. This library solved the problem of my solutions to captchas not registering as a human solution, and that enabled me to freely scrape the pages. 

### Others

The remaining stories and code explanations can be found in files themselves:

- [`Scraper`](./scraper.ipynb)
- [`Data Science`](./data_science.ipynb)