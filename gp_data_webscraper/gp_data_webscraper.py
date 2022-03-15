from urllib.request import urlopen
import ssl
import datetime
import argparse

import bs4

CONTEXT = ssl._create_unverified_context()

def _get_html(url) -> str:
    return urlopen(url, context=CONTEXT).read().decode("utf-8")

def _get_list_items(url) -> bs4.element.ResultSet:
    html = _get_html(url)
    soup = bs4.BeautifulSoup(html, features="html.parser")
    unordered_list = soup.find(id="dataset-resources").find("ul")
    list_items = unordered_list.find_all(recursive=False)
    return list_items

def _get_id(item) -> str:
    return item.get("data-id")

def _get_date(item) -> str:
    title = item.find("a", recursive=False).get("title").strip()
    date_str = title.split(" ")[-2] + " " + title.split(" ")[-1].replace(".csv", "")
    date = datetime.datetime.strptime(date_str, "%B %Y").strftime("%Y-%m")
    return date

def _get_url(item) -> str:
    return item.find("div", recursive=False).find("ul", recursive=False).find_all('li')[1].find("a").get("href")

def _get_dataset(item) -> dict:
    id = _get_id(item=item)
    date = _get_date(item=item)
    url = _get_url(item=item)
    dataset = {"id": id, "date": date, "url": url}
    return dataset

def _extract_list_datasets(list_items) -> list[dict]:
    list_datasets = []
    for item in list_items:
        dataset = _get_dataset(item=item)
        list_datasets.append(dataset.copy())
    return list_datasets

def _sort_list_datasets(list_datasets) -> list[dict]:
    return sorted(list_datasets, key=lambda d: d['date'], reverse=True)

def scrape_data(url) -> list[dict]:
    list_items = _get_list_items(url)
    list_datasets = _extract_list_datasets(list_items)
    sorted_list_datasets = _sort_list_datasets(list_datasets=list_datasets)
    return sorted_list_datasets

def __main() -> list[dict]:
    parser = argparse.ArgumentParser(description="Web Scraper for datasets with tag 'GP Practice' on OpenDataNI https://www.opendatani.gov.uk/.")
    parser.add_argument("url", type=str, help="url for webpage being scraped")
    args = parser.parse_args()
    print(*scrape_data(url=args.url), sep='\n')

if __name__ == "__main__":
    __main()