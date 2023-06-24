import requests
from bs4 import BeautifulSoup


def extract_remote_jobs(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        # write your ✨magical✨ code here
        results = []
        jobs = soup.find_all('tr', class_="job")
        for job_section in jobs:
            anchor = job_section.find('a', class_="preventLink")
            # print(anchor)
            link = anchor['href']
            title = job_section.select_one("a h2")
            company = job_section.select_one("span>h3")
            location = job_section.find("div", class_="location")
            job_data = {
                            'company': company.string.strip(),
                            'location': location.string.strip(),
                            'position': title.string.strip(),
                            'link': f"https://remoteok.com{link}"
                        }
            results.append(job_data)
        return results
    else:
        print("Can't get jobs.")
