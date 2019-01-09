class EventGenerator:
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

    def set_ids(self, **kwargs):
        if 'year_id' in kwargs:
            self.year_id = kwargs['year_id']

        if 'semester_id' in kwargs:
            self.semester_id = kwargs['semester_id']

        if 'tab_id' in kwargs:
            self.tab_id = kwargs['tab_id']

        if 'sel1_id' in kwargs:
            self.sel1_id = kwargs['sel1_id']

        if 'sel2_id' in kwargs:
            self.sel2_id = kwargs['sel2_id']

        if 'sel3_id' in kwargs:
            self.sel3_id = kwargs['sel3_id']

        if 'sel1_scrl_id' in kwargs:
            self.sel1_scrl_id = kwargs['sel1_scrl_id']

        if 'sel2_scrl_id' in kwargs:
            self.sel2_scrl_id = kwargs['sel2_scrl_id']

        if 'sel3_scrl_id' in kwargs:
            self.sel3_scrl_id = kwargs['sel3_scrl_id']

        if 'btn_id' in kwargs:
            self.btn_id = kwargs['btn_id']

    def get_ids(self):
        return {
            'year_id':      self.year_id,
            'semester_id':  self.semester_id,
            'tab_id':       self.tab_id,
            'sel1_id':      self.sel1_id,
            'sel2_id':      self.sel2_id,
            'sel3_id':      self.sel3_id,
            'sel1_scrl_id': self.sel1_scrl_id,
            'sel2_scrl_id': self.sel2_scrl_id,
            'sel3_scrl_id': self.sel3_scrl_id,
            'btn_id':       self.btn_id
        }

    def init(self):
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

    def select_year(self, year):
        # year
        # e.g. 2019
        return 'ComboBox_Select~E002Id~E004{}~E005Key~E004{}~E005ByEnter~E004false~E003~E002ResponseData~E004delta' \
               '~E005ClientAction~E004submit~E003~E002~E003'.format(self.year_id, year)

    def select_semester(self, semester_value):
        # semester_value
        # e.g. 090
        return 'ComboBox_Select~E002Id~E004{}~E005Key~E004{}~E005ByEnter~E004false~E003~E002ResponseData~E004delta' \
               '~E005ClientAction~E004submit~E003~E002~E003'.format(self.semester_id, semester_value)

    def select_tab(self, _tab_id):
        # _tab_id
        # e.g. WDE9
        return 'TabStrip_TabSelect~E002Id~E004{}~E005ItemId~E004{}~E005ItemIndex~E0040~E005FirstVisibleItemIndex' \
               '~E0040~E003~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003'.\
            format(self.tab_id, _tab_id)

    def select_sel(self, idx, value):
        # sel value with data-itemkey
        target = ''
        if idx is 1:
            target = self.sel1_id
        elif idx is 2:
            target = self.sel2_id
        elif idx is 3:
            target = self.sel3_id
        else:
            raise EventGeneratorException('index out of range on sel')

        return 'ComboBox_Select~E002Id~E004{}~E005Key~E004{}~E005ByEnter~E004false~E003~E002ResponseData' \
               '~E004delta~E005ClientAction~E004submit~E003~E002~E003'.format(target, value)

    def search(self):
        return 'Button_Press~E002Id~E004{}~E003~E002ResponseData~E004delta~E005ClientAction' \
               '~E004submit~E003~E002~E003'.format(self.btn_id)

    def status(self):
        n = lambda x: x or ''

        print("----------")
        print('[EventGenerator] ids: ')
        print('[EventGenerator] year_id: ' + n(self.year_id))
        print('[EventGenerator] semester_id: ' + n(self.semester_id))
        print('[EventGenerator] tab_id: ' + n(self.tab_id))
        print('[EventGenerator] sel1_id: ' + n(self.sel1_id))
        print('[EventGenerator] sel2_id: ' + n(self.sel2_id))
        print('[EventGenerator] sel3_id: ' + n(self.sel3_id))
        print('[EventGenerator] btn_id: ' + n(self.btn_id))
        print("----------")


class EventGeneratorException(Exception):
    def __init__(self, msg):
        self.message = msg
