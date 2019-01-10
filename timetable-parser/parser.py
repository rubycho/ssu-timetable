from browser import Browser
from event_generator import EventGenerator
from config import *

from enum import Enum
from bs4 import BeautifulSoup

import ast


class Parser:
    def __init__(self):
        self.browser = Browser()
        self.event_generator = EventGenerator()

        self.data = {}
        self.selections = {}

        for item in ParserActions:
            self.data[item] = ''
            self.selections[item] = []
        self.max_sel = 0

        self.browser.connect()
        self.status()

    # SAP 시스템에 액션을 보냄.
    def action(self, what, value):
        if self.check_invalid_what(what):
            raise ParserException('Undefined Action')

        if what == ParserActions.INIT:
            response = self.browser.request(self.event_generator.init())
            self.data[what] = response

            tmp = BeautifulSoup(response, 'lxml')

            # find input element by current value
            year_input = tmp.find(value=CURRENT_YEAR_VALUE)
            semester_input = tmp.find(value=CURRENT_SEMESTER_VALUE)
            tabs = tmp.find_all(action='TAB_ACCESS', ct="TSITM_standards")

            if year_input is None:
                raise ParserException('input for year not found')

            if semester_input is None:
                raise ParserException('input for semester not found')

            if len(tabs) < 1:
                raise ParserException('too short tab list')

            # get element ids, for SAP actions
            year_id = year_input['id']
            semester_id = semester_input['id']

            # TAB들의 parent가 가지고 있는 id를 input id로 취급하는 듯 함.
            # id="WDE8-panel"
            tab_input = tabs[0].find_parent()
            tab_id = tab_input['id'].replace('-panel', '')

            self.event_generator.set_ids(year_id=year_id, semester_id=semester_id, tab_id=tab_id)

            # add to selections
            self.selections[ParserActions.YEAR] = self.retrieve_selections_from_input(tmp, year_input)
            self.selections[ParserActions.SEMESTER] = self.retrieve_selections_from_input(tmp, semester_input)

            _tabs = []
            for sel in tabs:
                _tabs.append((sel['id'], sel.get_text()))
            self.selections[ParserActions.TAB] = _tabs

        elif what == ParserActions.YEAR:
            # value = year (int)
            response = self.browser.request(self.event_generator.select_year(value))
            self.data[what] = response

        elif what == ParserActions.SEMESTER:
            # value = semester (itemkey, string)
            response = self.browser.request(self.event_generator.select_semester(value))
            self.data[what] = response

        elif what == ParserActions.TAB:
            # value = tab_id (id of tab, string)
            response = self.browser.request(self.event_generator.select_tab(value))
            self.data[what] = response

            tmp = BeautifulSoup(response, 'lxml')
            tab_selections = tmp.find(id=self.event_generator.get_ids()['tab_id']).find_all('input')
            search_button = tmp.find(title='찾기 ')

            self.set_tab_inner_selection_ids(tab_selections)
            self.parse_tab_inner_selections(tmp)
            self.event_generator.set_ids(btn_id=search_button['id'])

        elif what == ParserActions.SEL1 or what == ParserActions.SEL2 or what == ParserActions.SEL3:
            # value = data-itemkey
            idx = 0
            if what == ParserActions.SEL1:
                idx = 1
            elif what == ParserActions.SEL2:
                idx = 2
            elif what == ParserActions.SEL3:
                idx = 3

            if idx > self.max_sel:
                print("[Parser] index out of range; of max sel")
                print("[Parser] Do nothing :)")
                return

            response = self.browser.request(self.event_generator.select_sel(idx, value))
            self.data[what] = response

            tmp = BeautifulSoup(response, 'lxml')
            self.parse_tab_inner_selections(tmp)

        elif what == ParserActions.SEARCH:
            response = self.browser.request(self.event_generator.search())

            tmp = BeautifulSoup(response, 'lxml')
            table = tmp.find(id=MAIN_TABLE_ID)
            self.data[what] = table

    def get_data(self, what):
        if self.check_invalid_what(what):
            raise ParserException('Undefined Action')

        return self.data[what]

    def get_selection(self, what):
        if self.check_invalid_what(what):
            raise ParserException('Undefined Action')

        return self.selections[what]

    def parse_tab_inner_selections(self, bstype_body):
        keys = self.event_generator.get_ids()

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

    # tab 내부의 input id와 scrl id를 저장함.
    def set_tab_inner_selection_ids(self, bstype_tab_inner_selections):
        self.reset_tab_inner_selection_ids()

        selection_length = len(bstype_tab_inner_selections)
        if selection_length > 0:
            self.event_generator.set_ids(
                sel1_id=bstype_tab_inner_selections[0]['id'],
                sel1_scrl_id=self.retrieve_scrl_id_from_input(bstype_tab_inner_selections[0])
            )
            self.max_sel += 1
        if selection_length > 1:
            self.event_generator.set_ids(
                sel2_id=bstype_tab_inner_selections[1]['id'],
                sel2_scrl_id=self.retrieve_scrl_id_from_input(bstype_tab_inner_selections[1])
            )
            self.max_sel += 1
        if selection_length > 2:
            self.event_generator.set_ids(
                sel3_id=bstype_tab_inner_selections[2]['id'],
                sel3_scrl_id=self.retrieve_scrl_id_from_input(bstype_tab_inner_selections[2])
            )
            self.max_sel += 1

    def reset_tab_inner_selection_ids(self):
        self.event_generator.set_ids(
            sel1_id=None, sel2_id=None, sel3_id=None,
            sel1_scrl_id=None, sel2_scrl_id=None, sel3_scrl_id=None
        )
        self.max_sel = 0

    @staticmethod
    def retrieve_selections_from_input(bstype_body, bstype_input):
        scrl_id = Parser.retrieve_scrl_id_from_input(bstype_input)

        return Parser._retrieve_selections_from_input(bstype_body, scrl_id)

    @staticmethod
    def retrieve_scrl_id_from_input(bstype_input):
        # lsdata에서 selection items을 가지고 있는 element의 id를 가지고 있음.
        # 임의 값 8로 작성함.
        selection_id = ast.literal_eval(bstype_input['lsdata'])
        scrl_id = selection_id[8]

        return scrl_id

    @staticmethod
    def _retrieve_selections_from_input(bstype_body, scrl_id):
        selections = bstype_body.find(id=scrl_id + '-scrl').find_all(class_='lsListbox__value')

        _selections = []
        for sel in selections:
            _selections.append((sel['data-itemkey'], sel.get_text()))

        return _selections

    @staticmethod
    def check_invalid_what(what):
        if type(what) is not ParserActions:
            raise ParserException('what is not a ParserAction')

        return \
            what.value < ParserActions.INIT.value or \
            what.value > ParserActions.SEARCH.value

    def status(self):
        print("----------")
        print("[Parser] Successfully connected with SAP:")
        print("[Parser] secure_id: " + self.browser.get_secure_id())
        print("[Parser] context_id: " + self.browser.get_context_id())
        print("----------")

        self.event_generator.status()


class ParserActions(Enum):
    INIT = 0
    YEAR = 1
    SEMESTER = 2
    TAB = 3
    SEL1 = 4
    SEL2 = 5
    SEL3 = 6
    SEARCH = 7


class ParserException(Exception):
    def __init__(self, msg):
        self.message = msg
