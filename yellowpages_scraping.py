# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 07:30:24 2020

@author: anandadwiarifian
"""

import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome()
driver.get("https://yellowpages.co.id/")
assert "Yellowpages" in driver.title

# input the industry type that you wanna scrap
industry = "hotel"
time.sleep(3)
elem = driver.find_element_by_xpath("//input[@class='text src-keyword']")
elem.clear()
elem.send_keys(industry) 
time.sleep(3)
elem.send_keys(Keys.RETURN)
assert "Daftar" in driver.title

# Uncomment the line below if you want to disable sorting result by your current location
# driver.find_element_by_xpath("//a[contains(text(),'Hapus Lokasi')]").click()

# define list of data
listings_yellowpages = pd.DataFrame()

listing_names_all = []
listing_links_all = []
listing_types_all = []
listing_cities_all = []
listing_phones_all = []
listing_mails_all = []
listing_webs_all = []
listing_addresses_all = []

page = 1
while True:
    try:
        print('Page: '+str(page))
        assert "Daftar" in driver.title
        # time.sleep(3)
        
        # get data in the page
        listing_names = [i.text for i in driver.find_elements_by_xpath("//div[@class='col-md-5 home-list-pop-desc inn-list-pop-desc']/h4")]
        listing_types = [i.text for i in driver.find_elements_by_xpath("//div[@class='col-md-5 home-list-pop-desc inn-list-pop-desc']/h4/following-sibling::p[1]")]
        listing_addresses = [i.text for i in driver.find_elements_by_xpath("//div[@class='col-md-5 home-list-pop-desc inn-list-pop-desc']/h4/following-sibling::p[2]")]
        listing_cities = [i.text for i in driver.find_elements_by_xpath("//div[@class='col-md-5 home-list-pop-desc inn-list-pop-desc']/h4/following-sibling::p[3]")]
        listing_phones = [i.text for i in driver.find_elements_by_xpath("//div[@class='col-md-5 home-list-pop-desc inn-list-pop-desc']/h4/following-sibling::div[@class='row']")]
        listing_links = [i.get_attribute("href") for i in driver.find_elements_by_xpath("//div[@class='col-md-5 home-list-pop-desc inn-list-pop-desc']/ancestor::a")]
        listing_boxes = driver.find_elements_by_xpath("//div[@class='home-list-pop list-spac']")
        listing_mails = []
        listing_webs = []
        for i in listing_boxes:
            try:
                mailNweb_box = i.find_element_by_class_name("col-md-4.home-list-pop-desc.inn-list-pop-desc")
                try:
                    # listing_mail = mailNweb_box.find_element_by_tag_name('div').find_element_by_tag_name('ul').find_element_by_tag_name('li').find_element_by_partial_link_text('mail').get_attribute("href")
                    listing_mail = mailNweb_box.find_element_by_xpath("div/ul[1]/li/a[contains(text(),'mail')]").get_attribute("href")
                    listing_mail = listing_mail.replace("mailto:","")
                except:
                    listing_mail = None
                
                try:
                    listing_web = mailNweb_box.find_element_by_xpath("div/ul[2]/li/a[contains(text(),'site')]").get_attribute("href")
                    listing_web = listing_web.replace("?utm_campaign=yellowpagesutm_source=yellowpages&utm_medium=sponsored-listing","")
                except:
                    listing_web = None
            except:
                listing_mail = None
                listing_web = None
            listing_mails.append(listing_mail)
            listing_webs.append(listing_web)
                
        
        #extend data lists with data in this page
        listing_names_all.extend(listing_names)
        listing_cities_all.extend(listing_cities)
        listing_addresses_all.extend(listing_addresses)
        listing_types_all.extend(listing_types)
        listing_phones_all.extend(listing_phones)
        listing_mails_all.extend(listing_mails)
        listing_webs_all.extend(listing_webs)
        listing_links_all.extend(listing_links)

        # time.sleep(10)
        driver.find_element_by_xpath("//a[contains(text(),'Next')]").click()
        page+=1 # count page
        continue
    
    except NoSuchElementException:
        break
    
    # except Exception as ex:
    #     print("{0} {1}".format(type(ex).__name__, ex.args[0:150]))
    #     break

# close browser
# driver.close()

# save the data to DataFrame
listings_yellowpages['name'] = listing_names_all
listings_yellowpages['city'] = listing_cities_all
listings_yellowpages['address'] = listing_addresses_all
listings_yellowpages['type'] = listing_types_all
listings_yellowpages['phone'] = listing_phones_all
listings_yellowpages['mail'] = listing_mails_all
listings_yellowpages['web'] = listing_webs_all
listings_yellowpages['link'] = listing_links_all

# export to csv file
directory = 'G:/My Drive/Documents in Drive/scraping/listing_yellowpages_{0}.csv'.format(datetime.datetime.now().strftime("%d%m%Y"))
listings_yellowpages.to_csv(directory, encoding='utf-8', index = False)
