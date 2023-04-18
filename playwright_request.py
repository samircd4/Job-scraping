from playwright.sync_api import sync_playwright
import requests
from selectolax.parser import HTMLParser
import pandas as pd
import time


def getDetails(url, idx, term):
    error_link = 'error_link.txt'
    print(f'{idx} number page scraping started!')
    res = requests.get(url)
    html = HTMLParser(res.text)
    details = {}
    if res.status_code == 200:
        try:
            try:
                divs = html.css('div.job-info--permament-icons > div')
                title = html.css_first('div.job-info--container > h1').text().strip()
                location = divs[1].css_first('a > span').text().strip()
                salary = divs[0].css_first('span > span').text().strip()
                contract_type = divs[2].css_first('span > a').text()
                job_type = divs[2].css_first('span').text().split(',')[1].strip()
                description = html.css_first('div.branded-job--description-container > div > span').text()
                details['job_title'] = title
                details['location'] = location
                details['contract_type'] = contract_type
                details['job_type'] = job_type
                details['description'] = description
                details['salary'] = salary
                details['job_url'] = url
            except:
                title = html.css_first('.job-header.row h1').text().strip()
                location = html.css('div.location')[1].css('span')[1].css_first('a').text().strip()
                time = html.css('div.time')[1].css_first('span').text().split(',')
                contract_type = time[0].strip()
                job_type = time[1].strip()
                description = html.css_first('div.description > span').text().strip()
                salary = html.css('div.salary')[1].css_first('span > span').text().strip()
                
                details['job_title'] = title
                details['location'] = location
                details['contract_type'] = contract_type
                details['job_type'] = job_type
                details['description'] = description
                details['salary'] = salary
                details['job_url'] = url
            print(f'{idx} number page done!')
        except:
            with open(error_link, 'a') as f:
                f.write(f'{term}, {url}\n')
    else:
        print('Status code not 200 or OK')
    if len(details) == 0:
        return None
    return details

def getLinks(html_page):
    html = HTMLParser(html_page)
    link_list = html.css('section#server-results > article.job-result-card')
    links = []
    for idx, link in enumerate(link_list, start=1):
        base_url = 'https://www.reed.co.uk'
        url = link.css_first('h2.job-result-heading__title > a').attributes['href']
        links.append(f'{base_url}{url}')
    return links

def searchTitle(title):
    print(f'Bot going to search for {title}!')
    url = 'https://www.reed.co.uk/jobs'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000)
        page.goto(url)
        
        page.get_by_role("button", name="I Accept").click()
        page.wait_for_timeout(500)
        page.locator("#keywords").click()
        page.wait_for_timeout(500)
        page.locator("#keywords").fill(title)
        page.get_by_role("button", name="Search jobs").click()
        page.wait_for_timeout(5000)
        
        
        first_page = getLinks(page.content())
        all_links = [link for link in first_page]
        
        for i in range(1,20):
            try:
                page.get_by_role("link", name="Next").click()
                # print(lik.is_disabled)
                page.wait_for_timeout(3000)
                links = getLinks(page.content())
                for link in links:
                    all_links.append(link)
                
                print(f'page number {i} is done')
            except:
                print(f'page number {i} is not found')
                break
        # page.wait_for_timeout(5000)
        
        browser.close()
    return all_links

def saveToCsv(data, term):
    filename= term.replace(' ', '_')
    df = pd.DataFrame(data)
    df.to_csv(f'{filename}.csv', index=False)

def getTitles(txt_file):
    with open(txt_file) as f:
        lines = f.readlines()
        titles = []
        for line in lines:
            titles.append(line.strip())
    return titles

def main():
    txt_file = 'titles.txt'
    titles = getTitles(txt_file)
    for term in titles[:28]:
        curr_time = time.time()
        print(f'Title: {term} Scraping started!')
        links = searchTitle(term)
        data = []
        for idx, link in enumerate(links, start=1):
            try:
                job = getDetails(link, idx, term)
            except:
                print(f'Title: {term} not success!')
            if job is not None:
                data.append(job)
        saveToCsv(data, term)
        new_time = time.time()
        time_taken = new_time - curr_time
        print(f'Consumed: {time_taken}')


if __name__ == '__main__':
    main()