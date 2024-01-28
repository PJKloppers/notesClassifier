import requests
from bs4 import BeautifulSoup
import json
def clean_web_content(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text


    if response.status_code != 200:
        raise Exception(f'Error getting content from {url}. Status code: {response.status_code}')



    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    code_tags = soup.find_all('code')
    title = soup.title.string

    citations = []
    cite = soup.find_all('cite')
    for c in cite:
        text= c.get_text(' ', strip=True)
        text = text.replace('"', '')
        citations.append(text)
        c.extract()


    # class "w3-example" and 'w3-code' is used for code examples
    for element in soup.find_all(class_=['w3-code']):
        code_tags.append(element)
        element.extract()

    tables= []

    for table in soup.find_all('table'):

        column_names = []
        rows = []
        for th in table.find_all('th'):
            col = th.get_text(strip=True).replace('\n', '')
            if col:
                column_names.append(col)

        if not column_names:
            table.extract()
            continue

        for tr in table.find_all('tr'):
            row_values = []
            for td in tr.find_all('td'):
                txt = td.get_text(strip=True).replace('\n', ' ')
                row_values.append(txt)


            # if  the list is not empty
            if row_values:
                rows.append(row_values)


        tables.append({
            'column_names': column_names,
            'rows': rows
        })
        table.extract()


    used_headings = []
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        # if the heading contians a <a> tag, remove it
        for a in heading.find_all('a'):
            a.extract()
        heading_text = heading.get_text(strip=True).replace('[]', '')
        used_headings.append(heading_text)





    for element in soup.find_all('meta'):
        element.extract()

    # Remove hidden elements
    for element in soup.find_all(style=lambda value: value and 'hidden' in value.lower()):
        element.extract()

    # Remove <div> tags created by ads or recommended sections
    for element in soup.find_all('div', class_=['ad', 'recommendation']):
        element.extract()

    # Remove all links
    for element in soup.find_all('a'):
        element.extract()

    for element in soup.find_all('form'):
        element.extract()

    for element in soup.find_all('input'):
        element.extract()

    for element in soup.find_all('button'):
        element.extract()


    # Remove elements with certain classnames
    classnames_to_remove = ['ad', 'sponsor', 'sponsors__name']
    for class_name in classnames_to_remove:
        for element in soup.find_all(class_=class_name):
            element.extract()

    # remove  the content inside <code> tags
    for tag in soup.find_all('code'):
        tag.extract()

    # Get the cleaned content
    cleaned_content = soup.get_text(separator=" ", strip=True)


    Code = []
    for code_tag in code_tags:
        code_content = code_tag.get_text(separator=' ', strip=True)
        if code_content.count(' ') >= 2:
            Code.append(code_tag.get_text(separator=' ', strip=True))


    return {
        'title': title,
        'content': cleaned_content,
        'code_snippets': Code,
        'citations': citations,
        'tables': tables,
        'headings': used_headings,
        'url': url,
    }

if __name__ == '__main__':
    # url = "https://www.w3schools.com/html/default.asp"
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    # url = "https://www.researchgate.net/publication/281137332_Atomsk_A_tool_for_manipulating_and_converting_atomic_data_files"
    # url = "https://414.reii.co.za"
    # url = "https://www.google.com/search?q=something"
    url = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"
    content = clean_web_content(url)

    print(json.dumps(content, indent=4))




#################################

# import requests
# from bs4 import BeautifulSoup
#
# class WebCleaner:
#     def __init__(self, url, classnames_to_remove=None):
#         self.url = url
#         self.classnames_to_remove = classnames_to_remove or []
#
#     def _fetch_html_content(self):
#         try:
#             response = requests.get(self.url)
#             response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             print(f"Error getting content from {self.url}. Exception: {e}")
#             return None
#
#         return response.text
#
#     def _remove_elements_by_class(self, soup):
#         for class_name in self.classnames_to_remove:
#             for element in soup.find_all(class_=class_name):
#                 element.extract()
#
#     def clean_web_content(self):
#         html_content = self._fetch_html_content()
#
#         if not html_content:
#             return None
#
#         soup = BeautifulSoup(html_content, 'html.parser')
#
#         code_tags = soup.find_all('code')
#         title = soup.title.string
#
#         citations = [c.get_text(' ', strip=True).replace('"', '') for c in soup.find_all('cite')]
#         self._remove_elements_by_class(soup)
#
#         for element in soup.find_all(class_=['w3-code']):
#             code_tags.append(element)
#             element.extract()
#
#         tables = []
#
#         for table in soup.find_all('table'):
#             column_names = [th.get_text(strip=True).replace('\n', '') for th in table.find_all('th')]
#
#             if not column_names:
#                 table.extract()
#                 continue
#
#             rows = [[td.get_text(strip=True).replace('\n', ' ') for td in tr.find_all('td')] for tr in table.find_all('tr') if tr.find_all('td')]
#             tables.append({
#                 'column_names': column_names,
#                 'rows': rows
#             })
#             table.extract()
#
#         used_headings = [heading.get_text(strip=True).replace('[]', '') for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
#
#         for element in soup.find_all(['meta', lambda tag: tag.has_attr('style') and 'hidden' in tag['style'].lower(), 'div', 'a', 'form', 'input', 'button']):
#             element.extract()
#
#         for tag in soup.find_all('code'):
#             tag.extract()
#
#         cleaned_content = soup.get_text(separator=" ", strip=True)
#
#         Code = [code_tag.get_text(separator=' ', strip=True) for code_tag in code_tags if code_tag.get_text(separator=' ', strip=True).count(' ') >= 2]
#
#         return {
#             'title': title,
#             'content': cleaned_content,
#             'code_snippets': Code,
#             'citations': citations,
#             'tables': tables,
#             'headings': used_headings,
#             'url': self.url,
#         }

# if __name__ == '__main__':
#     url = "https://en.wikipedia.org/wiki/Web_scraping"
#     web_cleaner = WebCleaner(url)
#     content = web_cleaner.clean_web_content()
#
#     print(content)
