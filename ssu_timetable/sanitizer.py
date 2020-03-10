from typing import List
from bs4 import BeautifulSoup


class Sanitizer:
    """
    Parser로 모은 데이터를 깔끔하게 Python 객체로 변환한다.
    """
    @staticmethod
    def replace_space(text: str):
        return text.replace('\xa0', ' ')

    @staticmethod
    def table_to_list(data: str) -> List[List[str]]:
        """
        SEARCH의 결과를 dict형 리스트로 변환한다.
        :param data: SEARCH result
        """

        # change br tag as \r\n, \xa0 as space
        p_data = data.replace('<br>', '\r\n')\
            .replace('<br/>', '\r\n')\
            .replace('<br />', '\r\n')\
            .replace('\xa0', ' ')

        ret_list = []
        soup = BeautifulSoup(p_data, 'lxml')
        trs = soup.find_all('tr')

        if len(trs) < 2:
            raise SanitizerException('no data to convert.')

        # header
        ths = trs[0].find_all('th')
        ret_list.append([x.text for x in ths])

        # rows
        for tr in trs[1:]:
            tds = tr.find_all('td')
            tmp = [x.text for x in tds]
            if len(tmp) > 1:
                ret_list.append(tmp)
        return ret_list


class SanitizerException(Exception):
    def __init__(self, msg):
        self.message = msg
