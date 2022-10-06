####################################################
# This project web scrapes data science vacancies
# in Germany to find out which skills and softwares
# are the most demanded

# libaries
from selenium import webdriver
import time
import pandas as pd

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# uncomment if you want to run the broswer in headless mode
# set headless option
# headOption = webdriver.FirefoxOptions()
# headOption.add_argument('-headless')

# Load the web driver and get the url
driver = webdriver.Firefox(executable_path = "path\\geckodriver.exe")   # insert the path where your geckodriver is saved
driver.maximize_window()
driver.implicitly_wait(15)

# Enter to the site
driver.get('https://www.linkedin.com/login')
time.sleep(10)

# Accepting cookies
driver.find_element_by_xpath('/html/body/div/main/div[1]/div/section/div/div[2]/button[1]').click()
time.sleep(4)

# User Credentials
# add your email address and password in 'insert email address' and 'insert password' respectively
elementID = driver.find_element_by_id('username')
elementID.send_keys('insert email address')
time.sleep(6)

elementID = driver.find_element_by_id('password')
elementID.send_keys('insert password')
time.sleep(5)

elementID.submit()
time.sleep(7)

# go to job postings
driver.find_element(By.XPATH, '/html/body/div[7]/header/div/nav/ul/li[3]/a').click()
time.sleep(5)

# go to job posting website
url = 'https://www.linkedin.com/jobs/search/?geoId=101282230&keywords=data%20science&location=Germany&refresh=true'
driver.get(url)
time.sleep(7)

# Obtaining all the job posting links
links = []
print('Collecting jon posting links')
try:
    for page in range(2, 10): # loop needs to start at the current page + 1
        time.sleep(2)
        try:
            jobs_block = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')  # page changes sometimes, which is why I use try & except
        except:
            jobs_block = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
        jobs_list = jobs_block.find_elements(By.CSS_SELECTOR, '.ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item')

        # collects the links in the a tag and appends them to a list
        for job in jobs_list:
            total_links = job.find_elements(By.TAG_NAME, 'a')
            for a in total_links:
                time.sleep(1)
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute(
                        'href') not in links:
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scrolls down to each job posting
            driver.execute_script("arguments[0].scrollIntoView();", job)

        print(f'Collected links of page: {page - 1}')
        time.sleep(4)
        try:
            driver.find_element(By.XPATH, f"//button[@aria-label='Page {page}']").click()
        except:
            driver.find_element(By.XPATH, f'"/html/body/div[7]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/ul/li[{page}]/button"').click()
        print('clicked next page')
except:
    pass
print('Found ' + str(len(links)) + ' links for job offers')

# creating empty lists to append desired data to later
job_titles = []
company = []
company_size = []
location = []
work_type = []
level = []
job_desc = []

i = 0
j= 1

# going to each scraped link and get the desired information
for i in range(len(links)):
    try:
        driver.get(links[i])
        i = 1 + i
        time.sleep(3)
        # Click 'See more'
        try:
            WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[7]/div[3]/div/div[1]/div[1]/div/div[2]/footer/button/span'))).click()
        except:
            driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[1]/div[1]/div/div[4]/footer/button/span').click()
        print('clicked')
    except:
        pass

    # Finding the desired information
    infos = driver.find_elements(By.CLASS_NAME, 'p5')
    for info in infos:
        try:
            job_titles.append(info.find_element(By.TAG_NAME, 'h1').text)
            company.append(info.find_element(By.CLASS_NAME, 'jobs-unified-top-card__company-name').text) # or class ember-view t-black t-normal
            location.append(info.find_element(By.CLASS_NAME, 'jobs-unified-top-card__bullet').text)
            work_type.append(info.find_element(By.CLASS_NAME, 'jobs-unified-top-card__workplace-type').text)
            j += 1
        except:
            pass
        time.sleep(2)
        
    # scraping job descriptions
    job_descriptions = driver.find_elements(By.CSS_SELECTOR, '.jobs-description__container.jobs-description__container--condensed')
    for job_description in job_descriptions:
        job_desc.append(job_description.find_element(By.TAG_NAME, 'span').text)
        print(f'Scraping job desc {j}')
        time.sleep(2)


# creating the dataframe
columns = ['job_title', 'company', 'location', 'work_type', 'job_desc']
df = pd.DataFrame(list(zip(job_titles, company, location, work_type, job_desc)), columns=columns)

# saving the data in a csv file
df.to_csv(r'job_postings.csv', index=False)

driver.quit()
