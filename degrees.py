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
        self.source = 'Analytics NCSU'
        self.source_url = 'https://analytics.ncsu.edu/?page_id=4184'
        self.source_notes = []

        self.first_enrolled = html.find_previous('h3').string #TODO: Save only integer year
        self.url = html.a['href']
        html.a.clear()
        print(html)
