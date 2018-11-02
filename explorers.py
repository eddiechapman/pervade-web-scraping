from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from degrees import AnalyticsNCSUDegree, DataSciGradProgramsDegree, EdisonProjectDegree


class Explorer:

    def __init__(self):
        self.degrees = []
        self.target_elements = []

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
                    print('good response:   ', url)
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
        self.generate_degrees()

    def generate_degrees(self):
        response = self.request_html(self.url)
        soup = BeautifulSoup(response, 'html.parser')
        starting_point = soup.find(string="CHRONOLOGY OF GRADUATE PROGRAMS IN ANALYTICS AND DATA SCIENCE")
        p_tags = starting_point.find_all_next('p')
        for tag in p_tags:
            degree = AnalyticsNCSUDegree(tag)
            self.degrees.append(degree)
            degree.to_json()


class DataSciGradProgramsExplorer(Explorer):

    def __init__(self):
        super()
        self.degrees = []
        self.url = 'https://www.datasciencegraduateprograms.com/school-listing/#context/api/listings/prefilter'
        self.generate_degrees()

    def generate_degrees(self):
        response = self.request_html(self.url)
        soup = BeautifulSoup(response, 'html.parser')
        starting_point = soup.find('div', class_='stateheader-departments')
        a_tags = starting_point.find_all_next('a', href=True)
        if a_tags:
            for tag in a_tags:
                degree = DataSciGradProgramsDegree(tag)
                self.degrees.append(degree)
                degree.to_json()


class EdisonProjectExplorer(Explorer):

    def __init__(self):
        super()
        self.url = 'http://edison-project.eu/university-programs-list'
        self.edison_urls = []
        self.degree_urls = []
        self.degrees = []

        self.generate_edison_urls()
        self.collect_degree_urls()
        self.generate_degrees()

    def generate_degrees(self):
        for url in self.degree_urls:
            response = self.request_html(url)
            soup = BeautifulSoup(response, 'html.parser')
            degree = EdisonProjectDegree(soup, url)
            self.degrees.append(degree)
            degree.to_json()

    def collect_degree_urls(self):
        for url in self.edison_urls:
            response = self.request_html(url)
            soup = BeautifulSoup(response, 'html.parser')
            td_tags = soup.find_all('td', class_='views-field views-field-title')
            if td_tags:
                a_tags = [td.find('a', href=True) for td in td_tags]
                for a in a_tags:
                    self.degree_urls.append(a.get('href'))

    def generate_edison_urls(self):
        self.edison_urls.append(self.url)
        for i in range(1, 14):
            self.edison_urls.append(self.url+'?page='+str(i))

