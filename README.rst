"""""""""""""""""
GP Data Web Scraper
"""""""""""""""""

-------------------------
A web scraper for datasets in OpenDataNI https://www.opendatani.gov.uk/
-------------------------

-------
Dependencies
-------

- Poetry

-------
Installation
-------

Navigate to root directory and run `poetry install`

-------
Test
-------

From root directory run `poetry run pytest`

-------
Run
-------

This web scraper works for the following url's:

- https://www.opendatani.gov.uk/dataset/gp-practice-list-sizes
- https://www.opendatani.gov.uk/dataset/gp-prescribing-data

From root directory run `poetry run python3 gp_data_webscraper "<url>"`
