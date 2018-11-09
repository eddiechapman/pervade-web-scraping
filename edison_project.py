from functions import get_page, to_json


def generate_source_urls():
    '''
    Create URLs for each page of the source's degree list.
    '''
    url = 'http://edison-project.eu/university-programs-list'

    # Source URLs for pages 1-13
    source_urls = [url + '?page=' + str(i) for i in range(1, 14)]

    # Add the starting page to the beginning of the list
    source_urls = [url] + source_urls

    return source_urls


def extract_degree_links():
    '''
    Find URLs that lead to degree pages.
    '''
    degree_urls = []
    for url in source_urls:
        soup = get_page(url)
        if soup:
            for td in soup.find_all('td', class_='views-field views-field-title'):
                url = td.find('a', href=True).get('href')
                degree_urls.append('http://edison-project.eu' + url)

    return degree_urls


def extract_degree_info():
    '''
    Extract and store information about individual degrees by visiting degree URLs.
    '''
    degrees = []

    for url in degree_urls:
        soup = get_page(url)
        if not soup:
            continue
        degree = {'url': url, 'source': 'Edison Project University Programs List'}

        # Degree name
        a = soup.header.h1.find('a', string=True)
        if a:
            degree['degree'] = a.string

        try:
            strings = [tag for tag in soup.main.stripped_strings]
            for i, string in enumerate(strings):
                if string.split()[0].endswith(':'):
                    degree[string.strip(':').lower()] = strings[i+1]
        except AttributeError:
            pass

        degrees.append(degree)
        to_json(degree)

    return degrees


if __name__ == '__main__':
    source_urls = generate_source_urls()
    degree_urls = extract_degree_links()
    degrees = extract_degree_info()




