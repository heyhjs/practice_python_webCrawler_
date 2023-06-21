from bs4 import BeautifulSoup
from selenium import webdriver


def extract_indeed_jobs(keyword):
    browser = webdriver.Chrome()
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        browser.get(f'{base_url}?q={keyword}&start={page*10}')
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find('ul', class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)
        for job in jobs:
            zone = job.find('div', class_='mosaic-zone')
            if zone == None:
                anchor = job.select_one("h2 a")
                link = anchor['href']
                title = anchor['aria-label']
                company = job.select_one("span.companyName").string
                region = job.select_one("div.companyLocation").string
                job_data = {
                    'company': company.replace(',', ' '),
                    'location': region.replace(',', ' '),
                    'position': title.replace(',', ' '),
                    'link': f"https://kr.indeed.com{link}"
                }
                results.append(job_data)
    return results


def get_page_count(keyword):
    browser = webdriver.Chrome()
    base_url = "https://kr.indeed.com/jobs?q="
    browser.get(f'{base_url}{keyword}')
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find('nav', attrs={"aria-label": "pagination"})
    pages = pagination.find_all('div', recursive=False)
    count = (len(pages))
    if count == 0:
        return 1
    else:
        return count - 1
