import _thread
import csv
import sys
from urllib.request import urlopen

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
        return {
            'name': '',
            'region': '',
            'style': '',
            'brewery': ''
        }
    mui_elems = header_div.find('.MuiTypography-root')
    links = header_div.find('a')
    return {
        'name': mui_elems[0].text,
        'region': mui_elems[1].text,
        'style': links[0].text,
        'brewery': links[1].text
    }



def write_reviews(file_number, start_range, end_range):
    with open('beer_reviews'+file_number+'.csv', mode='a') as csv_file:
        fieldnames = ['name', 'region', 'style', 'brewery', 'review']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        for i in range(start_range, end_range):
            parse_beer_page(i,writer)


def parse_beer_page(number,writer):
    session = HTMLSession()

    url = 'https://www.ratebeer.com/beer/{}/'.format(str(number + 1))
    try:
        page = session.get(url)
        page.html.render(script=injected_script)
        row = {}
        for key, value in get_beer_params(page.html).items():
            row[key] = value
        if row['name'] != '':
            reviews_divs = page.html.find(
                '.BeerReviewListItem___StyledDiv-iilxqQ>.Text___StyledTypographyTypeless-bukSfn')
            reviews = [review.text for review in reviews_divs]

            for review in reviews:
                write_row = row.copy()
                write_row['review'] = review
                writer.writerow(write_row)
    except:
        return
    finally:
        session.close()
        print(number)

injected_script = get_script_expanding_reviews_code()

scanning_range = end_range - start_range
starting_file_number = 1
try:
    for i in range(4):
        start_scanning = start_range + i * scanning_range
        end_scanning = end_range + i * scanning_range
        _thread.start_new_thread(write_reviews, (starting_file_number + i, start_scanning, end_scanning))
except:
    print("Nie umiesz w wielowatkowość, pogódź się z tym")
