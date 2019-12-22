import pprint


class EventGenerator:
    """
    SAPEVENTQUEUE에 해당하는 스트링을 생성하는 클래스.
    상호작용 해야하는 element의 id를 관리하는 클래스.
    """
    def __init__(self):
        self.year_id = None
        self.semester_id = None
        self.tab_id = None

        self.sel1_id = None
        self.sel2_id = None
        self.sel3_id = None

        self.sel1_scrl_id = None
        self.sel2_scrl_id = None
        self.sel3_scrl_id = None

        self.btn_id = None

    def get_ids(self):
        return self.__dict__

    def set_ids(self, **kwargs):
        self.__dict__.update(kwargs)

    def reset_sel_ids(self):
        """
        콤보박스에 해당하는 id들을 초기화한다.
        """
        self.sel1_id = self.sel2_id = self.sel3_id = None
        self.sel1_scrl_id = self.sel2_scrl_id = self.sel3_scrl_id = None

    def init(self) -> str:
        return 'ClientInspector_Notify~E002Id~E004WD01~E005Data~E004ClientWidth~003A326px~003BClientHeight~003A956px' \
              '~003BScreenWidth~003A1920px~003BScreenHeight~003A1080px~003BScreenOrientation~003Alandscape' \
              '~003BThemedTableRowHeight~003A21px~003BThemedFormLayoutRowHeight~003A25px~003BDeviceType~003ADESKTOP' \
              '~E003~E002ResponseData~E004delta~E005EnqueueCardinality~E004single~E003~E002~E003' \
              '~E001Custom_ClientInfos~E002Id~E004WD01~E005WindowOpenerExists~E004false~E005ClientURL~E004http' \
              '~003A~002F~002Fecc.ssu.ac.kr~002Fsap~002Fbc~002Fwebdynpro~002Fsap~002Fzcmw2100~003Fsap-language~003DKO' \
              '~0023~E005ClientWidth~E004326~E005ClientHeight~E004956~E005DocumentDomain~E004ssu.ac.kr' \
              '~E005IsTopWindow~E004true~E005ParentAccessible~E004true~E003~E002ClientAction~E004enqueue' \
              '~E005ResponseData~E004delta~E003~E002~E003~E001LoadingPlaceHolder_Load~E002Id~E004_loadingPlaceholder_' \
              '~E003~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003'

    def select_year(self, year: int) -> str:
        # year
        # e.g. 2019
        return 'ComboBox_Select~E002Id~E004{}~E005Key~E004{}~E005ByEnter~E004false~E003' \
               '~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003'\
            .format(self.year_id, year)

    def select_semester(self, semester_value: str) -> str:
        # semester_value
        # e.g. 090
        return 'ComboBox_Select~E002Id~E004{}~E005Key~E004{}~E005ByEnter~E004false~E003' \
               '~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003'\
            .format(self.semester_id, semester_value)

    def select_tab(self, _tab_id: str) -> str:
        # _tab_id
        # e.g. WDE9
        return 'TabStrip_TabSelect~E002Id~E004{}~E005ItemId~E004{}~E005ItemIndex~E0040~E005FirstVisibleItemIndex' \
               '~E0040~E003~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003' \
            .format(self.tab_id, _tab_id)

    def select_sel(self, idx: int, value: str) -> str:
        # sel value with data-itemkey
        if idx is 1:
            target = self.sel1_id
        elif idx is 2:
            target = self.sel2_id
        elif idx is 3:
            target = self.sel3_id
        else:
            raise EventGeneratorException('index out of range on sel')

        return 'ComboBox_Select~E002Id~E004{}~E005Key~E004{}~E005ByEnter~E004false~E003' \
               '~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003'\
            .format(target, value)

    def search(self) -> str:
        return 'Button_Press~E002Id~E004{}~E003~E002ResponseData~E004delta~E005ClientAction' \
               '~E004submit~E003~E002~E003'.format(self.btn_id)

    def status(self):
        print("=======================")
        print('[EventGenerator] ids: ')
        pprint.pprint(self.__dict__)
        print("=======================")


class EventGeneratorException(Exception):
    def __init__(self, msg):
        self.message = msg
