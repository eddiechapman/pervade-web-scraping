from functions import get_page, to_json

def extract_degree_info():

    degrees = []
    url = 'https://www.datasciencegraduateprograms.com/school-listing/#context/api/listings/prefilter'
    soup = get_page(url)
    if not soup:
        return

    for tag in soup.find('div', class_='stateheader-departments').find_all_next('a', href=True):

        degree = {'url': url, 'source': 'Data Science Graduate Programs'}

        # Degree title
        parent = tag.parent
        if parent:
            degree['degree'] = parent.string

        # Degree university
        h3 = tag.find_previous('h3', string=True)
        if h3:
            degree['university'] = h3.string

        # Degree department
        strong = tag.find_previous('strong', string=True)
        if strong:
            degree['department'] = strong.string

        # Degree URL
        degree['url'] = tag.get('href')

        # Degree state
        h2 = tag.find_previous('h2', string=True)
        if h2:
            degree['state'] = h2.string

        # Misc. properties of degree
        ul = tag.find_next('ul')
        if ul:
            degree['properties'] = [li.string for li in ul.find_all('li')]

        # Degree accredidation info
        em = tag.find_next('em', string=True)
        if em:
            degree['accredidation'] = em.string

        degrees.append(degree)
        to_json(degree)

    return degrees


if __name__ == '__main__':
    degrees = extract_degree_info()