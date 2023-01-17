import datetime
from unittest.mock import MagicMock
import pytest
from gp_data_ni_webscraper import webscraper

@pytest.mark.integration
def test_non_existent_endpoint():
    with pytest.raises(ValueError) as value_error:
        webscraper.scrape_data("https://www.opendatani.gov.uk/dataset/non-existent-endpoint")

@pytest.mark.integration
def test_scrape_data_gp_practice_list_sizes():
    dataset_list = webscraper.scrape_data("https://www.opendatani.gov.uk/dataset/gp-practice-list-sizes")
    assert type(dataset_list) is list and len(dataset_list) > 0

@pytest.mark.integration
def test_scrape_data_gp_prescribing_data():
    dataset_list = webscraper.scrape_data("https://www.opendatani.gov.uk/dataset/gp-prescribing-data")
    assert type(dataset_list) is list and len(dataset_list) > 0

@pytest.mark.unit
def test_scrape_data_returns_data():
    with open("tests/fixtures/title-normal.html", "r") as file:
        html = file.read()
    webscraper._get_html = MagicMock(return_value=html)
    dataset_list = webscraper.scrape_data("https://www.mockeddomain.com/datasets")
    assert len(dataset_list) == 1 and dataset_list[0].get("id") == "1"

@pytest.mark.unit
def test_scrape_data_handles_title_with_csv_file_extension():
    with open("tests/fixtures/title-csv.html", "r") as file:
        html = file.read()
    webscraper._get_html = MagicMock(return_value=html)
    dataset_list = webscraper.scrape_data("https://www.mockeddomain.com/datasets")
    assert dataset_list[0].get("date") ==  datetime.datetime(year=2022, month=2, day=1).strftime("%Y-%m")
