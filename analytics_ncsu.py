from functions import get_page, to_json


def extract_degree_info():

    degrees = []
    url = 'https://analytics.ncsu.edu/?page_id=4184'
    soup = get_page(url)
    if not soup:
        return

    degree_header = soup.find(string="CHRONOLOGY OF GRADUATE PROGRAMS IN ANALYTICS AND DATA SCIENCE")
    p_tags = degree_header.find_all_next('p')
    for tag in p_tags:

        degree = {'url': url, 'source': 'Analytics NCSU'}

        # Degree title
        a = tag.find('a', string=True)
        if a:
            degree['degree'] = a.string

        # Degree URL
        a = tag.find('a', href=True)
        if a:
            degree['url'] = a.get('href')

        # First year of enrollment
        try:
            h3 = tag.find_previous('h3')
            degree['first_enrolled'] = int(h3.string.replace('\u2022', '').strip())
        except ValueError:
            degree['first_enrolled'] = None

        # University and department are found in a single string separated by commas.
        try:
            # Remove link tag to access university and department string in p tag.
            tag.a.decompose()
            text = tag.string.strip().split(',')
            text = [value.strip() for value in text if value is not '']
        except AttributeError:
            degree['university'] = None
            degree['department'] = None
        else:
            # Values can be assigned with certainty when there are only two commas.
            if len(text) is 2:
                degree['university'] = text[0]
                degree['department'] = text[1]

            # Otherwise (like when a university name includes a comma), both fields are
            # assigned the entire string and can be cleaned up later.
            else:
                degree['university'] = ','.join(text)
                degree['department'] = ','.join(text)

        degrees.append(degree)

    return degrees


if __name__ == '__main__':
    degrees = extract_degree_info()
    for degree in degrees:
        to_json(degree)