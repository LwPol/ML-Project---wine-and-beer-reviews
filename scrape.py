import csv
import sys
import asyncio
from urllib.request import urlopen
from concurrent.futures import ProcessPoolExecutor

from pyppeteer import launch
from requests_html import HTML


def retrieve_jquery_source():
    with urlopen('http://code.jquery.com/jquery-latest.min.js') as jquery:
        return jquery.read().decode('utf-8')


def get_script_expanding_reviews_code():
    jquery_src = retrieve_jquery_source()
    expand_reviews_script = """
        buttons = document.getElementsByClassName("MuiButtonBase-root MuiButton-root MuiButton-text Button___StyledMaterialButton-FZwYh kvPsnQ colorized__WrappedComponent-apsCh kAVjHC -ml-3 MuiButton-textPrimary");
        for (let i = 1; i < buttons.length; ++i) {
            $(buttons[i]).click();
        }
    """
    return jquery_src + expand_reviews_script


async def render_html(url, injected_script):
    browser = await launch()
    try:
        page = await browser.newPage()
        await page.goto(url)
        await page.evaluate(injected_script, force_expr=True)
        return await page.content()
    finally:
        await browser.close()


def get_page_html(url, injected_script):
    return asyncio.get_event_loop().run_until_complete(render_html(url, injected_script))


def get_beer_params(html):
    header_div = html.find('.fj-s.fa-c.mb-4', first=True)
    if header_div is None:
        return None
    mui_elems = header_div.find('.MuiTypography-root')
    links = header_div.find('a')
    return {
        'name': mui_elems[0].text,
        'region': mui_elems[1].text,
        'style': links[0].text,
        'brewery': links[1].text
    }

class BeerPageParser:
    def __init__(self, injected_script):
        self.injected_script = injected_script

    def parse_beer_page(self, number):
        url = 'https://www.ratebeer.com/beer/{}/'.format(str(number + 1))
        try:
            print(number)
            html = HTML(html=get_page_html(url, self.injected_script))
            beer = get_beer_params(html)
            if beer is not None:
                reviews_divs = html.find(
                    '.BeerReviewListItem___StyledDiv-iilxqQ>.Text___StyledTypographyTypeless-bukSfn')
                beer['reviews'] = [review.text for review in reviews_divs]
            return beer
        except Exception as ex:
            print(ex)
            print("Error on beer id", number + 1, file=sys.stderr)
            return None

beer_parser = BeerPageParser(get_script_expanding_reviews_code())

def drink_beer(beer_number):
    return beer_parser.parse_beer_page(beer_number)


def write_reviews(file_number, start_range, end_range):
    with open('beer_reviews' + str(file_number) + '.csv', mode='a', newline='') as csv_file, ProcessPoolExecutor() as pool:
        fieldnames = ['name', 'region', 'style', 'brewery', 'review']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        for beer in pool.map(drink_beer, range(start_range, end_range)):
            if beer is None:
                continue
            for review in beer['reviews']:
                row = {key: entry for key, entry in beer.items() if key != 'reviews'}
                row['review'] = review
                writer.writerow(row)

if __name__ == '__main__':
    start_range = int(sys.argv[1])
    end_range = int(sys.argv[2])
    file_num = int(sys.argv[3])
    write_reviews(file_num, start_range, end_range)
