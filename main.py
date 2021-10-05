from contextlib import closing
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
from time import sleep
import json


def parse(text):
    return text.replace('$', '').replace(',', '')


list_checking = ['cardano', 'solana', 'polkadot-new', 'terra-luna', 'algorand',
                 'axie-infinity', 'monero', 'amp', 'just', 'bora', 'dkargo', 'sentinel-protocol', 'everipedia']

with closing(Firefox()) as browser:
    for link in list_checking:
        browser.get(
            f'https://coinmarketcap.com/currencies/{link}/historical-data/')
        sleep(10)

        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(5)
        browser.execute_script(
            'document.querySelector(".statsItemRight").scrollIntoView();')
        sleep(5)

        browser.find_element_by_class_name('gqItsT').click()
        sleep(10)

        browser.find_elements_by_class_name('jaVFYH li')[-1].click()
        sleep(10)

        browser.execute_script(
            'document.querySelectorAll(".cEEOTh")[1].click();')
        sleep(10)

        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(10)

        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        rows = soup.find_all('tr')
        final_data = {}

        id_counter = 0

        for row in rows[1:]:
            row_data = row.get_text('^').split('^')
            object_to_add = {
                "day": row_data[0],
                "open": parse(row_data[1]),
                "high": parse(row_data[2]),
                "low": parse(row_data[3]),
                "close": parse(row_data[4]),
                "volume": parse(row_data[5]),
                "mkt cap.": parse(row_data[6])
            }

            final_data[id_counter] = object_to_add

            id_counter += 1

        json_data = json.dumps(final_data)

        with open(f"{link} historical.json", "w") as outfile:
            outfile.write(json_data)
