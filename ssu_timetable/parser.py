import ast
from enum import Enum
from typing import List, Tuple

from bs4 import BeautifulSoup

from .browser import Browser
from .config import Config
from .event_generator import KeyStore, EventGenerator


class ParserActions(Enum):
    INIT = 0
    YEAR = 1
    SEMESTER = 2
    TAB = 3
    SEL1 = 4
    SEL2 = 5
    SEL3 = 6
    SEARCH = 7
    LINE = 8


class Parser:
    """
    MAIN SAINT PARSER.
    """
    def __init__(self, config: Config):
        self.config = config
        self.browser = Browser()
        self.keystore = KeyStore()

        self.data = {}
        self.selections = {}

        for item in ParserActions:
            self.data[item] = ''
            self.selections[item] = []
        self.max_sel = 0

        self.browser.connect()

    def action(self, what: ParserActions, value: any):
        """
        SAP에 이벤트를 보낸다.
        결과는 get_data, get_selection을 통해 확인할 수 있다.

        :param what: 수행할 이벤트
        :param value: 이벤트 생성할 때 필요한 파라미터. (e.g. 콤보박스에서 선택 시 콤보박스 옵션 값)
        """
        # 초기화 단계 액션
        # value: Don't care
        if what == ParserActions.INIT:
            response = self.browser.request(EventGenerator.init())
            self.data[what] = response

            tmp = BeautifulSoup(response, 'lxml')

            # 학년도, 학기 input 찾기
            year_label = tmp.find('label', string='학년도')
            semester_label = tmp.find('label', string='학기')
            line_label = tmp.find('label', string='줄수 / 페이지')

            if year_label is None:
                raise ParserException('label for year not found')

            if semester_label is None:
                raise ParserException('label for semester not found')

            if line_label is None:
                raise ParserException('label for line not found')

            year_input = tmp.find(id=year_label['f'])
            semester_input = tmp.find(id=semester_label['f'])
            line_input = tmp.find(id=line_label['f'])

            # 탭 목록 찾기
            tabs = tmp.find_all(action='TAB_ACCESS', ct="TSITM_standards")
            if len(tabs) < 1:
                raise ParserException('too short tab list')

            # 이후 탭 선택 이벤트 시, 탭들의 parent가 가지고 있는 id를 사용해야 함
            # id="WDE8-panel"
            tab_input = tabs[0].find_parent()
            tab_id = tab_input['id'].replace('-panel', '')

            self.keystore.set_ids(
                year_id=year_input['id'],
                semester_id=semester_input['id'],
                line_id=line_input['id'],
                tab_id=tab_id
            )

            # 선택 가능한 학년도, 학기 아이템 추가
            self.selections[ParserActions.YEAR] = self.retrieve_selections_from_input(tmp, year_input)
            self.selections[ParserActions.SEMESTER] = self.retrieve_selections_from_input(tmp, semester_input)
            self.selections[ParserActions.LINE] = self.retrieve_selections_from_input(tmp, line_input)

            # 선택 가능한 탭 아이템 추가
            _tabs = []
            for sel in tabs:
                _tabs.append((sel['id'], sel.get_text()))
            self.selections[ParserActions.TAB] = _tabs

        # 줄 수 선택 액션
        # value: line (str), '10'
        elif what == ParserActions.LINE:
            response = self.browser.request(EventGenerator.combobox(self.keystore.line_id, str(value)))
            self.data[what] = response

        # 년도 선택 액션
        # value: year (int)
        elif what == ParserActions.YEAR:
            response = self.browser.request(EventGenerator.combobox(self.keystore.year_id, str(value)))
            self.data[what] = response

        # 학기 선택 액션
        # value: semester (itemkey, string)
        elif what == ParserActions.SEMESTER:
            response = self.browser.request(EventGenerator.combobox(self.keystore.semester_id, value))
            self.data[what] = response

        # 탭 선택 액션
        # value: tab_id (id of tab, string)
        elif what == ParserActions.TAB:
            response = self.browser.request(EventGenerator.tab(self.keystore.tab_id, value))
            self.data[what] = response

            # 결과를 바탕으로, 사용가능한 콤보박스와 버튼을 파악한다.
            tmp = BeautifulSoup(response, 'lxml')
            tab_selections = tmp.find(id=self.keystore.get_ids()['tab_id']).find_all('input')
            search_button = tmp.find(title='찾기 ')

            self.set_tab_inner_selection_ids(tab_selections)
            self.parse_tab_inner_selections(tmp)
            self.keystore.set_ids(btn_id=search_button['id'])

        # 탭 내부 콤보박스 액션
        # value = data-itemkey
        elif what == ParserActions.SEL1 or what == ParserActions.SEL2 or what == ParserActions.SEL3:
            idx = what.value - ParserActions.SEL1.value + 1
            if idx > self.max_sel:
                raise ParserException('index out of range: idx={}, max={}'.format(idx, self.max_sel))

            target = None
            if idx == 1:
                target = self.keystore.sel1_id
            elif idx == 2:
                target = self.keystore.sel2_id
            elif idx == 3:
                target = self.keystore.sel3_id

            response = self.browser.request(EventGenerator.combobox(target, value))
            self.data[what] = response

            # 선택 후에는 다음 콤보박스에 대한 옵션이 주어진다.
            tmp = BeautifulSoup(response, 'lxml')
            self.parse_tab_inner_selections(tmp)

        # 검색 액션
        # value: Don't care
        elif what == ParserActions.SEARCH:
            response = self.browser.request(EventGenerator.button(self.keystore.btn_id))

            tmp = BeautifulSoup(response, 'lxml')
            table = tmp.find(id=self.config.MAIN_TABLE_ID)
            self.data[what] = str(table)

    def get_data(self, what: ParserActions) -> str:
        return self.data[what]

    def get_selection(self, what: ParserActions) -> List[any]:
        return self.selections[what]

    def set_tab_inner_selection_ids(self, bstype_tab_inner_selections):
        """
        Tab 내부에 존재하는 콤보박스의 input 태그 id, scrl_id를 추출하고 저장한다.
        scrl_id는 콤보박스의 선택 옵션을 가지고 있는 element의 id이다.

        :param bstype_tab_inner_selections: Tab 내부의 input Tag List
        """
        self.reset_tab_inner_selection_ids()

        selection_length = len(bstype_tab_inner_selections)
        if selection_length > 0:
            self.keystore.set_ids(
                sel1_id=bstype_tab_inner_selections[0]['id'],
                sel1_scrl_id=self._retrieve_scrl_id_from_input(bstype_tab_inner_selections[0])
            )
            self.max_sel += 1
        if selection_length > 1:
            self.keystore.set_ids(
                sel2_id=bstype_tab_inner_selections[1]['id'],
                sel2_scrl_id=self._retrieve_scrl_id_from_input(bstype_tab_inner_selections[1])
            )
            self.max_sel += 1
        if selection_length > 2:
            self.keystore.set_ids(
                sel3_id=bstype_tab_inner_selections[2]['id'],
                sel3_scrl_id=self._retrieve_scrl_id_from_input(bstype_tab_inner_selections[2])
            )
            self.max_sel += 1

    def parse_tab_inner_selections(self, bstype_body):
        """
        Tab 내부의 콤보박스에서 선택할 수 있는 옵션들을 추출하고 저장한다.

        :param bstype_body: BeautifulSoup instance
        """
        keys = self.keystore.get_ids()

        if keys['sel1_scrl_id']:
            self.selections[ParserActions.SEL1] = self._retrieve_selections_from_input(
                bstype_body, keys['sel1_scrl_id'])
        if keys['sel2_scrl_id']:
            self.selections[ParserActions.SEL2] = self._retrieve_selections_from_input(
                bstype_body, keys['sel2_scrl_id']
            )
        if keys['sel3_scrl_id']:
            self.selections[ParserActions.SEL3] = self._retrieve_selections_from_input(
                bstype_body, keys['sel3_scrl_id']
            )

    def reset_tab_inner_selection_ids(self):
        """
        탭 상태가 변경된 경우, 콤보박스와 관련된 변수를 초기화한다.
        """
        self.keystore.reset_sel_ids()
        self.max_sel = 0

    @staticmethod
    def retrieve_selections_from_input(bstype_body, bstype_input) -> List[any]:
        """
        [콤보박스 input Tag를 이용하여] 콤보박스 선택 옵션들을 추출한다.

        :param bstype_body: BeautifulSoup instance
        :param bstype_input: 콤보박스 input Tag
        :return: 선택 옵션 Tuple List
        """
        scrl_id = Parser._retrieve_scrl_id_from_input(bstype_input)

        return Parser._retrieve_selections_from_input(bstype_body, scrl_id)

    @staticmethod
    def _retrieve_scrl_id_from_input(bstype_input) -> str:
        """
        콤보박스에서 scrl_id를 추출한다.

        :param bstype_input: 콤보박스 input Tag
        :return: scrl_id
        """
        # lsdata에서 selection items을 가지고 있는 element의 id를 가지고 있음.
        # 임의 값 8로 작성함.
        selection_id = ast.literal_eval(bstype_input['lsdata'])
        scrl_id = selection_id[8]

        return scrl_id

    @staticmethod
    def _retrieve_selections_from_input(bstype_body, scrl_id: str) -> List[Tuple]:
        """
        [scrl_id를 이용하여] 콤보박스의 선택 옵션들을 추출한다.

        :param bstype_body: BeautifulSoup instance
        :return: 선택 옵션 Tuple List
        """
        selections = bstype_body.find(id=scrl_id + '-scrl').find_all(class_='lsListbox__value')

        _selections = []
        for sel in selections:
            _selections.append((sel['data-itemkey'], sel.get_text()))

        return _selections

    def status(self):
        self.browser.status()
        self.keystore.status()


class ParserException(Exception):
    def __init__(self, msg):
        self.message = msg
