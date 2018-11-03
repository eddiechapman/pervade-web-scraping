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
        self.url = html.get('href')
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
            self.url = html.a.get('href')
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


class EdisonProjectDegree(Degree):

    def __init__(self, html, url):
        super()
        self.source = 'Edison Project University Programs List'
        self.source_url = url


        try:
            fields = {}
            tag = html.header.h1.find('a', string=True)
            self.degree = tag.string if tag is not None else None
            tags = [tag for tag in html.main.stripped_strings]
            for i in enumerate(tags):
                if tag.split(' ').endswith(':'):
                    fields[tag] = tags[i+1]
            self.country = fields.get('Country:')
            self.university = fields.get('University:')
            self.language = fields.get('Language:')
            self.degree_type = fields.get('Level:')
            if fields.get('Courses:'):
                self.courses = fields.get('Courses:').split(',')
            self.degree_url = fields.get('Link:')
            self.academic_title = fields.get('Title:')
            #print(json.dumps(fields, indent=2))
        except AttributeError:
            self.degree = None
            self.description = None
            self.country = None
            self.language = None
            self.university = None
            self.degree_type = None
            self.courses = None
            self.degree_url = None
            self.academic_title = None


