import requests
from bs4 import BeautifulSoup

# 웹 브라우저 user agent을 넣어주지 않으면 에러 발생
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'

URLS = {
    'BASE_URL': 'http://ecc.ssu.ac.kr',
    # 시간표 URL, extract SAP contexts (secure-id, contextid)
    'CONNECT_URL': 'http://ecc.ssu.ac.kr/sap/bc/webdynpro/sap/zcmw2100?sap-language=KO'
}


class Browser:
    def __init__(self):
        self.session = requests.Session()
        self.secure_id = None
        self.context_id = None

        self.session.headers.update({
            'User-Agent': USER_AGENT
        })

    def connect(self):
        r = self.session.get(URLS['CONNECT_URL'])

        soup = BeautifulSoup(r.text, 'html.parser')
        secure_id = soup.find(id='sap-wd-secure-id')
        context_id = soup.find(id='sap.client.SsrClient.form')

        if secure_id is None:
            raise BrowserException('sap-wd-secure-id not found')

        if context_id is None:
            raise BrowserException('sap-contextid not found')

        self.secure_id = secure_id['value']
        self.context_id = context_id['action']

    def request(self, command):
        r = self.session.post(
            URLS['BASE_URL'] + self.context_id,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'sap-charset': 'utf-8',
                'sap-wd-secure-id': self.secure_id,
                'SAPEVENTQUEUE': command
            }
        )

        if r.status_code != 200:
            print("Failed to run command: ")
            print(command)
            raise BrowserException('Request unsuccessful: ' + str(r.status_code))

        return r.text

    def get_secure_id(self):
        return self.secure_id

    def get_context_id(self):
        return self.context_id


class BrowserException(Exception):
    def __init__(self, msg):
        self.message = msg
