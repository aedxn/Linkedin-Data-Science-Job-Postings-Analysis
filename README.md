# Linkedin-Data-Science-Job-Postings-Analysis

This project is divided into two parts.

1. Web scraping Linkedin Data Scientist Roles using Selenium
2. Analysing the data 

The dataset only includes job openings for Germany.

### Web Scrpaing

The information scraped consists of:

* Job Title
* Company
* Location
* Work Type (remote/hybrid etc.)
* Job Description

### Data Analysis

Using my scraped data I created seniority levels based on the job title. As such, I created the following seniority levels:

* Intern
* Trainee
* Mid-Level
* Senior

Using Matplotlib and Seaborn I then visualised:

* The companies who offer most of the jobs
* The demanded skills, by role (Data Scientist, Data Analyst, Data Engineer
* The locations
* Work types by location (ie. remote vs. on-site)
