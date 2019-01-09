from parser import Parser, ParserActions

parser = Parser()
parser.action(ParserActions.INIT, 0)

print("YEAR SELECTIONS:")
print(parser.get_selection(ParserActions.YEAR))
print("SEMESTER SELECTIONS:")
print(parser.get_selection(ParserActions.SEMESTER))
print("TAB SELECTIONS:")
print(parser.get_selection(ParserActions.TAB))

parser.action(ParserActions.YEAR, '2019')
parser.action(ParserActions.SEMESTER, '090')

i = str(input('TAB KEY?'))
parser.action(ParserActions.TAB, i)
parser.status()

print("FIRST SELECTIONS:")
print(parser.get_selection(ParserActions.SEL1))

i = str(input('SEL1 KEY?'))
parser.action(ParserActions.SEL1, i)

print("SECOND SELECTIONS:")
print(parser.get_selection(ParserActions.SEL2))

i = str(input('SEL2 KEY?'))
parser.action(ParserActions.SEL2, i)

print("THIRD SELECTIONS:")
print(parser.get_selection(ParserActions.SEL3))

i = str(input('SEL3 KEY?'))
parser.action(ParserActions.SEL3, i)

print("Fetching...")
parser.action(ParserActions.SEARCH, None)

table = parser.get_data(ParserActions.SEARCH)

for td in table.find_all('tr'):
    if len(td.find_all('td')) < 2:
        continue
    print(td.text)
