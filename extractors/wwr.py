from bs4 import BeautifulSoup
from requests import get


def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f'{base_url}{keyword}')
    if response.status_code != 200:
        print("Can't request website")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all('section', class_="jobs")
    results = []
    for job in jobs:
        posts = job.find_all('li', class_="feature")
        for post in posts:
            anchors = post.find_all('a')
            anchor = anchors[1]
            link = anchor['href']
            company, kind, region = anchor.find_all('span', class_='company')
            title = anchor.find('span', class_='title')
            job_data = {
                'company': company.string.replace(',', ' '),
                'location': region.string.replace(',', ' '),
                'position': title.string.replace(',', ' '),
                'link': f"https://weworkremotely.com{link}"
            }
            results.append(job_data)
    return results
