from requests_html import HTMLSession
from urllib.request import urlopen
import sys

def print_usage():
    usage = """\
    Usage: {} [beer_id]
    """.format(sys.argv[0])
    print(usage)
    sys.exit(0)

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
    mui_elems = header_div.find('.MuiTypography-root')
    links = header_div.find('a')
    return {
        'name': mui_elems[0].text,
        'region': mui_elems[1].text,
        'style': links[0].text,
        'brewery': links[1].text
    }

if len(sys.argv) != 2:
    print_usage()

injected_script = get_script_expanding_reviews_code()

session = HTMLSession()

url = 'https://www.ratebeer.com/beer/{}/'.format(sys.argv[1])
page = session.get(url)
page.html.render(script=injected_script)

for key, value in get_beer_params(page.html).items():
    print('{}: {}'.format(key, value))
print()

reviews_divs = page.html.find('.BeerReviewListItem___StyledDiv-iilxqQ>.Text___StyledTypographyTypeless-bukSfn')
reviews = [review.text for review in reviews_divs]
print('\n-----------\n'.join(reviews))
