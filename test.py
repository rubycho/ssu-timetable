from browser import Browser

browser = Browser()
browser.connect()
init = browser.request('ClientInspector_Notify~E002Id~E004WD01~E005Data~E004ClientWidth~003A326px~003BClientHeight~003A956px~003BScreenWidth~003A1920px~003BScreenHeight~003A1080px~003BScreenOrientation~003Alandscape~003BThemedTableRowHeight~003A21px~003BThemedFormLayoutRowHeight~003A25px~003BDeviceType~003ADESKTOP~E003~E002ResponseData~E004delta~E005EnqueueCardinality~E004single~E003~E002~E003~E001Custom_ClientInfos~E002Id~E004WD01~E005WindowOpenerExists~E004false~E005ClientURL~E004http~003A~002F~002Fecc.ssu.ac.kr~002Fsap~002Fbc~002Fwebdynpro~002Fsap~002Fzcmw2100~003Fsap-language~003DKO~0023~E005ClientWidth~E004326~E005ClientHeight~E004956~E005DocumentDomain~E004ssu.ac.kr~E005IsTopWindow~E004true~E005ParentAccessible~E004true~E003~E002ClientAction~E004enqueue~E005ResponseData~E004delta~E003~E002~E003~E001LoadingPlaceHolder_Load~E002Id~E004_loadingPlaceholder_~E003~E002ResponseData~E004delta~E005ClientAction~E004submit~E003~E002~E003')
print(init)
