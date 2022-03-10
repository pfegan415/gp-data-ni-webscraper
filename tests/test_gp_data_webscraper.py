import datetime
from unittest.mock import MagicMock

from gp_data_webscraper import gp_data_webscraper


def test_scrape_data_returns_data():
    html = """<html>
                <section id=\"dataset-resources\">
                    <ul>
                        <li data-id=\"1\">
                            <a title=\"GP Practice Reference File - January 2022\">
                            </a>
                            <div>
                                <ul>
                                    <li>
                                    </li>
                                    <li>
                                        <a href=\"https://www.mockeddomain.com/datasets/dataset.csv\">
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </li>
                    </ul>
                </section>
            </html>"""
    gp_data_webscraper._get_html = MagicMock(return_value=html)
    dataset_list = gp_data_webscraper.scrape_data("https://www.mockeddomain.com/datasets")
    assert len(dataset_list) == 1 and dataset_list[0].get("id") == "1"


def test_scrape_data_handles_title_with_csv_file_extension():
    html = """<html>
                <section id=\"dataset-resources\">
                    <ul>
                        <li data-id=\"2\">
                            <a title=\"GP Practice Reference File - February 2022.csv\">
                            </a>
                            <div>
                                <ul>
                                    <li>
                                    </li>
                                    <li>
                                        <a href=\"https://www.mockeddomain.com/datasets/dataset.csv\">
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </li>
                    </ul>
                </section>
            </html>"""
    gp_data_webscraper._get_html = MagicMock(return_value=html)
    dataset_list = gp_data_webscraper.scrape_data("https://www.mockeddomain.com/datasets")
    assert dataset_list[0].get("date") ==  datetime.datetime(year=2022, month=2, day=1).strftime("%Y-%m")
