#!/usr/bin/env python


# Importing Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pymongo
import re
import pandas as pd

# Execute all of the scraping code from `mission_to_mars.ipynb` and return one Python dictionary containing all of the scraped data
def scrape():


    executable_path = {'executable_path': './chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)



    # Scraping Mars News 
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')





    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    # Display scrapped data 
    print(news_title)
    print(news_p)


    # Visit Mars Space Images through splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)



    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve background-image url from style tag 
    image_url = soup.find('article',class_='carousel_item')['style'].replace('background-image: url(','').replace(');', '')[1:-1]


    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'
    
    # Concatenate website url with scrapped route
    featured_image_url = main_url + image_url

    # Display full link to featured image
    featured_image_url



    # Scraping twitter page of Mars
    url = 'https://twitter.com/marswxreport?lang=en'

    # Browser visit
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html
    soup = bs(html, 'html.parser')



    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass



    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    mars_df = mars_df.set_index(['Description','Value'])
    # Save html code
    table_html = mars_df.to_html()


    # Display mars_df
    mars_df



    # Scraping Mars Hemispheres
    url_parent = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Browser visit
    browser.visit(url_parent)

    # Create a Beautiful Soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    # Child website links for each hemisphere
    base_url = "https://astrogeology.usgs.gov"
    links = [base_url + item.find(class_="description").a["href"] for item in soup.find_all("div", class_="item")]



    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []


    for url in links:
        
        # from url to soup
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # Extract data
        title = soup.find("div", class_="content").find("h2", class_="title").text.replace(" Enhanced", "")
        img_url = base_url + soup.find("img", class_="wide-image")["src"]
        
        # Store in list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    # Display hemisphere_image_urls
    print(hemisphere_image_urls)



    browser.quit()

     # Store in dictionary
    mars = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "table_html": table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Return results
    return mars





