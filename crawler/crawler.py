import os
import json
import pandas as pd
from selenium import webdriver
from tqdm import tqdm
from utils import DriverUtil

driver = webdriver.Firefox()
driver_util = DriverUtil(driver)

def get_coauthors():
    coauthor_xpath = "//li[@class='search__item card--shadow contrib-list__list']"
    coauthor_list = driver_util.get_multiple_element(coauthor_xpath)
    coauthors = []
    for coauth in coauthor_list:
        coauth_util = DriverUtil(coauth)
        try:
            name = coauth_util.get_single_element("./descendant::span[contains(@class, 'list__title')]")
            href = coauth_util.get_single_element("./descendant::a[@class='contrib-link']")
            weight = coauth_util.get_single_element("./descendant::div[@class='list__count hidden-xs']/child::a")
            profile = {
                'name': name.get_attribute('innerHTML'),
                'href': href.get_attribute('href'),
            }
            coauthors.append({
                'profile': profile,
                'weight': int(weight.get_attribute('innerHTML'))
            })
        except:
            pass
    return coauthors

def get_authors():
    author_xpath = "//div[contains(@class, 'people-list-container')]"
    author_list = driver_util.get_multiple_element(author_xpath)
    authors = []
    for author in author_list:
        author_util = DriverUtil(author)
        try:
            name = author_util.get_single_element("./descendant::div[contains(@class, 'name')]")

            profile_btn = author_util.get_single_element("./descendant::a[@class='view-profile']")
            author_dict = {
                'name': name.get_attribute('innerHTML'),
                'href': profile_btn.get_attribute('href'),
            }
            authors.append(author_dict)
        except:
            pass
    return authors

def iterate_pages(href, collect_data_fn):
    driver.get(f'{href}?pageSize=100')

    try:
        total = driver_util.get_single_element("//span[@class='result__count']")
        total = total.get_attribute('innerHTML')
        total = int(''.join([ i for i in total if i.isdigit() ]))
    except:
        return []

    results = []
    with tqdm(total=total) as pbar:
        while(len(results) < total):
            page_result = collect_data_fn()
            results.extend(page_result)
            pbar.update(len(page_result))

            if len(results) >= total:
                break

            # Next page
            next_btn = driver_util.get_multiple_element("//a[@class='pagination__btn--next']")
            if len(next_btn) == 0:
                break
            driver.get(next_btn[0].get_attribute('href'))
    return results

try:
    # Get list of people
    if os.path.exists('authors.json'):
        with open('authors.json', 'r') as f:
            graph = json.load(f)
        print(f'{len(graph.keys())} authors loaded')
        authors_list = [ { 'name': v['name'], 'href': k } for k,v in graph.items() ]
    else:
        print('Collecting authors...')
        authors_list = iterate_pages('https://dl.acm.org/people/is', get_authors)
        graph = { i['href']: { 'name': i['name'], 'adj': [] } for i in authors_list }
        print(f'{len(authors_list)} authors found!')
        with open('authors.json', 'w+') as f:
            json.dump(graph, f)

    print('Collecting coauthors...')
    for author in tqdm(authors_list):
        adj_file = os.path.join('graph', author["href"].split('/')[-1] + '.json')
        if os.path.exists(adj_file):
            continue
        try:
            coauthors = iterate_pages(f'{author["href"]}/colleagues', get_coauthors)
            with open(adj_file, 'w+') as f:
                json.dump(coauthors, f)
        except Exception as e:
            print(f'Error while collecting for author {author["name"]}')
            continue
except Exception as e:
    print(e)
    pass
finally:
    driver.quit()