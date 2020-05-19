def scrape():
    from bs4 import BeautifulSoup
    import requests
    import pymongo
    from splinter import Browser
    import pandas as pd
    import re
    import time
    #scrape news items
    url = 'https://mars.nasa.gov/news/'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find('li',class_='slide')
    content={}
    content['title'] = item.find('div', class_='content_title').a.text
    content['p']=item.find('div', class_='article_teaser_body').text
    # a=0
    # for i in item:
    #     content.append({})
    #     tit = i.find('div', class_='content_title').a.text
    #     par = i.find('div', class_='article_teaser_body').text
    #     content[a]['title']=tit
    #     content[a]['p']=par
    #     a=a+1
    browser.quit()
    #scrape image
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome',**executable_path,headless=False)
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    article=soup.find('article',class_='carousel_item')
    url_2 = article.a.get('data-fancybox-href')
    url_2=url_2.replace('mediumsize','largesize')
    url_2=url_2.replace('ip','hires')
    featured_image_url=url.split('/space')[0]+url_2
    browser.quit()
    #scrape weather
    url='https://twitter.com/marswxreport?lang=en'
    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome',**executable_path,headless=False)
    browser.visit(url)
    time.sleep(5)
    soup=BeautifulSoup(browser.html,'html.parser')
    tweet=soup.find_all('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    p=re.compile('^InSight')
    mars_weather=''
    for x in tweet:
        if p.match(x.text):
            mars_weather=x.text
            break
    browser.quit()
    #scrape space facts
    url='https://space-facts.com/mars/'
    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome',**executable_path)
    browser.visit(url)
    soup=BeautifulSoup(browser.html,'html.parser')
    table=soup.find('table')
    # data=pd.read_html(str(table))
    data=str(table)
    browser.quit()
    #scrape hemisphere images
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path={'executable_path':'chromedriver.exe'}
    browser=Browser('chrome',**executable_path)
    browser.visit(url)
    hemisphere_image_urls ={'Cerberus':{},'Schiaparelli':{},
                        'Syrtis':{},'Valles':{}}
    for x in hemisphere_image_urls:
        browser.click_link_by_partial_text(x)
        soup=BeautifulSoup(browser.html,'html.parser')
        title=soup.find('h2',class_='title').text
        hemisphere_image_urls[x]['title']=title
        url_hold=soup.find_all('a')
        for i in url_hold:
            if i.text=='Sample':
                hemisphere_image_urls[x]['img_url']=i.get('href')
                browser.back()
    browser.quit()
    mars = {}
    mars["news"]=content
    mars["image_url"]=featured_image_url
    mars["weather"] =mars_weather
    mars["facts"] = data
    mars["hemisphere"]=hemisphere_image_urls
    return mars
