from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from degrees import AnalyticsNCSUDegree, DataSciGradProgramsDegree


class Explorer:

    def __init__(self):
        self.degrees = []

    def request_html(self, url):
        """
        Download html content from 'url' using HTTP GET request.

        :return: html
        :return: none
        :exception: RequestException
        """
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    print('good response')
                    return resp.content
                else:
                    return None

        except RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    @property
    def degree_count(self):
        return len(self.degrees)


class AnalyticsNCSUExplorer(Explorer):

    def __init__(self):
        super()
        self.degrees = []
        self.url = 'https://analytics.ncsu.edu/?page_id=4184'
        self.response = self.request_html(self.url)
        self.soup = BeautifulSoup(self.response, 'html.parser')
        self.starting_point = self.soup.find(string="CHRONOLOGY OF GRADUATE PROGRAMS IN ANALYTICS AND DATA SCIENCE")
        self.degree_tags = self.starting_point.find_all_next('p')
        self.generate_degrees()

    def generate_degrees(self):
        for tag in self.degree_tags:
            degree = AnalyticsNCSUDegree(tag)
            self.degrees.append(degree)
            degree.to_json()


class DataSciGradProgramsExplorer(Explorer):

    def __init__(self):
        super()
        self.degrees = []
        self.url = 'https://www.datasciencegraduateprograms.com/school-listing/#context/api/listings/prefilter'
        self.response = self.request_html(self.url)
        self.soup = BeautifulSoup(self.response, 'html.parser')
        self.starting_point = self.soup.find('div', class_='stateheader-departments')
        self.degree_tags = self.starting_point.find_all_next('a', href=True)
        self.generate_degrees()

    def generate_degrees(self):
        for tag in self.degree_tags:
            degree = DataSciGradProgramsDegree(tag)
            self.degrees.append(degree)
            degree.to_json()


class EdisonProjectExplorer(Explorer):

    def __init__(self):
        super()
        self.degrees = []
        self.url = 'http://edison-project.eu/university-programs-list'
        self.response = self.request_html(self.url)
        self.soup = BeautifulSoup(self.response, 'html.parser')

        # TODO:
        # self.starting_point =
        # self.degree_tags = self.starting_point.find_all_next('a', href=True)
        self.generate_degrees()

    def generate_degrees(self):
        for tag in self.degree_tags:
            degree = EdisonProjectDegree(tag)
            self.degrees.append(degree)
            degree.to_json()