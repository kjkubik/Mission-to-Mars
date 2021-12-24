from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Creating an instance of a Splinter browser (prepping automated browser)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Give the url of the site we want to scrape with splinter?
# Here we are visiting the Mars NASA news site:
url = 'https://redplanetscience.com/'
browser.visit(url)
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')

# search for elements with a specific combination of tag (div) and attribute (list_text)
slide_elem = news_soup.select_one('div.list_text')
slide_elem

# This variable holds a ton of information, so look inside of that information to find this specific data.
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# Only RETURN title of the news article and not any of the HTML tags or elements
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
news_paragraph

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parsing the 2nd window so that we can continue scraping
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Add base URL of image and include the img_url
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html() 

# end the session
browser.quit()

# Starter code begins here
# I have deleted what was created in lesson and is not needed anymore

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(4, 12, 2):
    # get to the page you need to go to via anchors tags using index
    to_click = browser.find_by_tag('a')[x] 
    to_click.click()
    
    # define an empty dictionary
    a_dict = {}
    
    # parse resulting html using Soup
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
    
    # append the dictionaries to your list
    hemisphere_image_urls.append(a_dict)
    
    #go back to the first page
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()