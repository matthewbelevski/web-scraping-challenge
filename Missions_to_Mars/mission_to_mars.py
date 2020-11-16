# Dependencies
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time



def scrape_info():
    
    #sets the chromedriver path and opens the chromedriver browser
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    
    url_mn = 'https://mars.nasa.gov/news'
    
    #opens chromedriver browser to webpage
    browser.visit(url_mn)
    
    #allows a delay to let the page load fully before getting the HTML Object
    time.sleep(25)
    
    # HTML object and parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #returns the relevant div
    results = soup.find('div', class_='image_and_description_container')
    
    #finds the text of the news preview
    news_p = results.find("div", class_="rollover_description_inner").text
    
    #finds the text of the title
    news_title = results.find("h3").text
    
    #next url
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    #opens chromedriver browser to webpage
    browser.visit(url_jpl)
    
    
    #click the full image button
    browser.click_link_by_partial_text('FULL IMAGE')

    #click the more info button to get to the page with the high res image
    browser.click_link_by_partial_text('more info')
    
    #access the HTML with BeautifulSoup to store the high res image to the variable
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    
    #saves the image to the variable
    image_highres_url = soup2.find("img", class_="main_image")["src"]
    
    
    #combine the browser link with the image link to get a clickable link to the image and display the link
    featured_image_url = f"https://www.jpl.nasa.gov{image_highres_url}"
    
    #next webpage
    url_mf = "https://space-facts.com/mars/"
    
    browser.visit(url_mf)
    
    #finds the different tables on the website
    tables = pd.read_html(url_mf)
    
    #selects the first table
    df = tables[0]
    
    #rename columns from 0 and 1 to Description and Mars
    df = df.rename(columns = {0: "Description", 1: "Mars"})
    
    #set index to Description column
    df.set_index("Description", inplace = True)
    
    #set the class and border when saving to a HTML file
    df.to_html('table.html', classes = 'table table-striped table-hover', border = 0)
    
    #save HTML string for the table
    html_table = df.to_html(classes = 'table table-striped table-hover', border = 0)
    
    
    #list of hemisphere names for the browser to search through
    mars_hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Marineris"]
    
    #create the list that will store the dictionaries
    mars_dict = []

    #url and opens the chromedriver browser
    url_mh = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    browser.visit(url_mh)

    #for loop to search through the url
    for hem in mars_hemispheres:

        #lick the link with the name in the mars_hemispheres list
        browser.click_link_by_partial_text(hem)

        # HTML object and parse HTML with Beautiful Soup
        html3 = browser.html
        soup3 = BeautifulSoup(html3, 'html.parser')

        #retreive the title element, drop the word "Enhanced" and the space before it and then store into dictionary 
        title = soup3.find("h2", class_="title").text
        t = title.replace(" Enhanced", "")
        mars_dict.append({"title": t})

        #retreive the image url element, combine it with the url link and store it into dictionary
        image_link = soup3.find("img", class_="wide-image")["src"]
        url_image_link = f"https://astrogeology.usgs.gov{image_link}"
        mars_dict.append({"img_url": url_image_link})

        #goes back to the home page to start the search for the next hemisphere in the list
        browser.visit(url_mh)
        
    #save variables collected through the script into the dictionary
    mars_data = {
        "news_headline": news_title,
        "news_preview": news_p,
        "featured_image": featured_image_url,
        "info": html_table,
        "hemispheres": mars_dict
    }
    
    #close the broswer
    browser.quit()
    
    return mars_data
