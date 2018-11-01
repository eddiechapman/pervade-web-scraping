from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from degrees import AnalyticsNCSUDegree, DataSciGradProgramsDegree


class Explorer:

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


class AnalyticsNCSUExplorer(Explorer):

    def __init__(self):
        super()
        self.url = 'https://analytics.ncsu.edu/?page_id=4184'

        response = self.request_html(self.url)
        soup = BeautifulSoup(response, 'html.parser')
        starting_point = soup.find(string="CHRONOLOGY OF GRADUATE PROGRAMS IN ANALYTICS AND DATA SCIENCE")

        for tag in starting_point.find_all_next('p'):
            degree = AnalyticsNCSUDegree(tag)
            degree.to_json()


class DataSciGradProgramsExplorer(Explorer):

    def __init__(self):
        super()
        self.url = 'https://www.datasciencegraduateprograms.com/school-listing/#context/api/listings/prefilter'

        response = self.request_html(self.url)
        soup = BeautifulSoup(response, 'html.parser')
        starting_point = soup.find('div', class_='stateheader-departments')

        for degree in starting_point.find_all_next('a', href=True):
            degree = DataSciGradProgramsDegree(degree)
            degree.to_json()
