import requests
from bs4 import BeautifulSoup
import json



class WebCleaner:
    def __init__(self, url, classnames_to_remove=['nav', 'footer', 'sidebar', 'header', 'menu', 'menu-bar', 'menu__bar','w3-bar', 'menu-bar__item', 'menu', 'menu__item','top__nav', 'top__nav__item', 'top__nav__list','subtopnav','w3-sidebar']):
        self.url = url
        self.classnames_to_remove = classnames_to_remove or []
        self.tables = []
        self.citations = []
        self.code_snippets = []
        self.headings = []
        self.title = None



    def _fetch_html_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error getting content from {self.url}. Exception: {e}")
            return None

        return response.text

    def _remove_elements_by_class(self, soup):
        for class_name in self.classnames_to_remove:
            for element in soup.find_all(class_=class_name):
                print(f"Removing element with class {class_name}")
                print(element.get_text(separator=" ", strip=True))
                element.extract()

    def clean_web_content(self):
        html_content = self._fetch_html_content()

        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')


        code_tags = soup.find_all('code')

        for element in soup.find_all('div', class_=['w3-code']):
            code_tags.append(element)
            element.extract()

        self.title = soup.title.string

        citations = [c.get_text(' ', strip=True).replace('"', '') for c in soup.find_all('cite')]
        self._remove_elements_by_class(soup)

        for element in soup.find_all(class_=['w3-code']):
            code_tags.append(element)
            element.extract()

        #  Get the tables in the web page.
        tables = []
        for table in soup.find_all('table'):
            column_names = [th.get_text(strip=True).replace('\n', '') for th in table.find_all('th')]

            if not column_names:
                table.extract()
                continue

            rows = [[td.get_text(strip=True).replace('\n', ' ') for td in tr.find_all('td')] for tr in table.find_all('tr') if tr.find_all('td')]
            tables.append({
                'column_names': column_names,
                'rows': rows
            })
            table.extract()
        self.tables = tables
        del tables

        used_headings = [heading.get_text(strip=True) for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        self.headings = used_headings
        del used_headings


        # Remove al
        for element in soup.find_all(['meta', lambda tag: tag.has_attr('style') and 'hidden' in tag['style'].lower(), 'a', 'form', 'input', 'button']):
            element.extract()

        for tag in soup.find_all('code'):
            tag.extract()

        cleaned_content = soup.get_text(separator=" ", strip=True)

        Code = [code_tag.get_text(separator=' ', strip=True) for code_tag in code_tags]

        return {
            'title': self.title,
            'content': cleaned_content,
            'code_snippets': Code,
            'citations': citations,
            'tables': self.tables,
            'headings': self.headings,
            'url': self.url,
        }

if __name__ == '__main__':
    # url = "https://en.wikipedia.org/wiki/Web_scraping"
    # url = "https://pypi.org/project/beautifulsoup4/"
    url = "https://www.w3schools.com/html/html_tables.asp"
    web_cleaner = WebCleaner(url)
    content = web_cleaner.clean_web_content()

    print(json.dumps(content, indent=4))
