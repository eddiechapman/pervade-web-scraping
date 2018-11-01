import json


class Degree:

    def to_json(self):
        print(json.dumps(self.__dict__, indent=2))


class DataSciGradProgramsDegree(Degree):

    def __init__(self, html):
        super()
        self.source = 'Data Science Graduate Programs'
        self.source_url = 'https://www.datasciencegraduateprograms.com/school-listing/#context/api/listings/prefilter'
        self.source_notes = []

        self.degree = html.parent.string
        self.university = html.find_previous('h3').string
        self.department = html.find_previous('strong').string
        self.url = html['href']
        self.state = html.find_previous('h2').string
        self.properties = [tag.string for tag in html.find_next('ul').find_all('li')]
        self.accredidation = html.find_next('em').string


class AnalyticsNCSUDegree(Degree):

    def __init__(self, html):
        super()
        self.tag = str(html)
        self.source = 'Analytics NCSU'
        self.source_url = 'https://analytics.ncsu.edu/?page_id=4184'
        self.source_notes = []
        try:
            self.url = html.a["href"]
        except Exception:
            self.url = None

        try:
            self.first_enrolled = int(html.find_previous('h3').string.replace('\u2022', '').strip())
        except Exception:
            self.first_enrolled = None

        try:
            self.degree = html.a.string
        except Exception:
            self.degree = None

        try:
            html.a.decompose()
            text = html.string.strip().split(',')
            text = [text.strip() for text in text if text is not '']
            if len(text) is 2:
                self.university = text[0]
                self.department = text[1]
            else:
                self.university = ','.join(text)
                self.department = ','.join(text)
        except Exception:
            self.university = None
            self.department = None



