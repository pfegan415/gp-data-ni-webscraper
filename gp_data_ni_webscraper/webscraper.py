from urllib.request import urlopen
import ssl
import datetime
import argparse
import logging
import bs4

CONTEXT = ssl._create_unverified_context()
LOGGER = logging.getLogger(__name__)

def _get_html(url) -> str:
    LOGGER.info(f"Making request to url: {url}")
    return urlopen(url, context=CONTEXT).read().decode("utf-8")

def _get_list_items(html) -> bs4.element.ResultSet:
    LOGGER.info("Getting list items")
    soup = bs4.BeautifulSoup(html, features="html.parser")
    list_items = soup.find_all("div", {"class": "item flex flex-col gap-3 lg:flex-row items-start mb-8 lg:justify-between"})
    LOGGER.info(f"Retrieved {len(list_items)}")
    return list_items

def _get_id(item) -> str:
    return item.find("a").attrs['href'].split("/r/")[1]

def _get_date(item) -> str:
    title = item.find("a").text.strip()
    date_str = title.split(" ")[-2] + " " + title.split(" ")[-1].replace(".csv", "")
    return datetime.datetime.strptime(date_str, "%B %Y").strftime("%Y-%m")


def _get_url(item) -> str:
    return item.find("a", {"class": "py-1 px-6 ml-2 bg-blue-c-600 rounded-lg"}).attrs["href"]

def _get_dataset(item) -> dict:
    return {"id": _get_id(item=item), "date": _get_date(item=item), "url": _get_url(item=item)}

def _extract_list_datasets(result_set) -> list[dict]:
    list_datasets = []
    for item in result_set:
        dataset = _get_dataset(item=item)
        list_datasets.append(dataset.copy())
    return list_datasets

def _sort_list_datasets(list_datasets) -> list[dict]:
    LOGGER.info("Sorting dataset by date (descending)")
    return sorted(list_datasets, key=lambda d: d['date'], reverse=True)

def scrape_data(url) -> list[dict]:
    """
    Takes a url and returns list of dictionaries containing dataset id, date, and url for downloading the dataset as a csv file. List is ordered by date descending.
        Parameters:
            url (str): a url referencing a webpage in OpenDataNI
        Returns:
            sorted_list_datasets (list[dict]): a list of dictionaries with keys (id, date, url) ordered by date descending
    """
    html = _get_html(url)
    list_items = _get_list_items(html)
    list_datasets = _extract_list_datasets(list_items)
    return _sort_list_datasets(list_datasets=list_datasets)

def __main() -> list[dict]:
    parser = argparse.ArgumentParser(description="Web Scraper for datasets with tag 'GP Practice' on OpenDataNI https://www.opendatani.gov.uk/.")
    parser.add_argument("url", type=str, help="url for webpage being scraped")
    args = parser.parse_args()
    print(*scrape_data(url=args.url), sep='\n')

if __name__ == "__main__":
    __main()