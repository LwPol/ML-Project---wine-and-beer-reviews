import csv
import sys
from urllib.request import urlopen
from multiprocessing import Pool

from requests_html import HTMLSession

start_range = int(sys.argv[1])
end_range = int(sys.argv[2])


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
        print("parser created")
        self.injected_script = injected_script

    def parse_beer_page(self, number):
        url = 'https://www.ratebeer.com/beer/{}/'.format(str(number + 1))
        try:
            print(number)
            session = HTMLSession()
            page = session.get(url)
            page.html.render(script=self.injected_script, sleep=1)
            beer = get_beer_params(page.html)
            if beer is not None:
                reviews_divs = page.html.find(
                    '.BeerReviewListItem___StyledDiv-iilxqQ>.Text___StyledTypographyTypeless-bukSfn')
                beer['reviews'] = [review.text for review in reviews_divs]
            return beer
        except Exception as ex:
            print(ex)
            print("Error on beer id", number + 1, file=sys.stderr)
            return None
        finally:
            session.close()

beer_parser = BeerPageParser(get_script_expanding_reviews_code())

def drink_beer(beer_number):
    return beer_parser.parse_beer_page(beer_number)


def write_reviews(file_number, start_range, end_range):
    with open('beer_reviews' + str(file_number) + '.csv', mode='a', newline='') as csv_file, Pool(4) as pool:
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
    write_reviews(5, start_range, end_range)
