import datetime
from unittest.mock import MagicMock

import pytest

from gp_data_webscraper import gp_data_webscraper

@pytest.mark.unit
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

@pytest.mark.unit
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

@pytest.mark.integration
def test_scrape_data_gp_practice_list_sizes():
    dataset_list = gp_data_webscraper.scrape_data("https://www.opendatani.gov.uk/dataset/gp-practice-list-sizes")
    assert type(dataset_list) is list and len(dataset_list) > 0

@pytest.mark.integration
def test_scrape_data_gp_prescribing_data():
    dataset_list = gp_data_webscraper.scrape_data("https://www.opendatani.gov.uk/dataset/gp-prescribing-data")
    assert type(dataset_list) is list and len(dataset_list) > 0