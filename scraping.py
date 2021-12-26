# Import Splinter, BeautifulSoup, Pandas, and webdriver_manager for Chrome
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Creating an instance of a Splinter browser (prepping automated browser)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheric_data": mars_hemispheres(browser)
    }

    return data

# Scrape the titles and teasers from redplanetscience.com
def mars_news(browser):
    # Give the url of the site being to scrape with splinter
    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Delay loading of page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try: 
        # search for elements with tag (div) using attribute (list_text)
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first `a` tag and save it as `news_title`
        # Only RETURN title of the news article and not any of the HTML tags or elements
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError: 
        return None, None
        
    return news_title, news_paragraph

# Scrape Mars Data: Featured Image (10.3.4)
def featured_image(browser):
    # Give the url of the site being to scrape
    url = 'https://spaceimages-mars.com'
    # Visit the site
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parsing the 2nd window so that we can continue scraping
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError: 
        return None    
    
    # Add base URL of image and include the img_url to name the absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Scrape Mars and Earth Facts Table
def mars_facts():
    try: 
        # More-less a copy-paste of the table we want
        # Create a dataframe of the table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
 
    # Assign columns and set index of dataframe   
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert it to HTML (more-less)
    return df.to_html(classes="table table-striped")

# Scrape Mars Hemispheric Image and Title
def mars_hemispheres(browser):
    
    # initial page   
    url = 'https://marshemispheres.com/'
    browser.visit(url)
        
    hemisphere_image_urls = []
    
    for x in range(4, 12, 2):
        # goto page you need scrap data from
        to_click = browser.find_by_tag('a')[x] 
        to_click.click()
    
        # define an empty dictionary
        a_dict = {}
    
        # parse resulting html
        html = browser.html
        products_soup = soup(html, 'html.parser')
    
        # get the image
        product_jpeg = products_soup.find('div', class_='wide-image-wrapper')
        jpeg = product_jpeg.find('a').get('href')
        jpeg_with_parent = f'{url}{jpeg}'
    
        # get the title
        product_title = products_soup.find('div', class_='cover')
        title = product_title.find('h2',class_='title').text
    
        # put image and title into the dictionary 
        a_dict['img_url'] =  jpeg_with_parent
        a_dict['title'] = title
    
        # append the dictionary to your list
        hemisphere_image_urls.append(a_dict)
    
        #go back to initial page so that you can get next 
        browser.back()
    
    hemisphere_image_urls
    
    # end browser session
    browser.quit()        
    return hemisphere_image_urls    

if __name__ == "__main__":
    # scrape data
    print(scrape_all())