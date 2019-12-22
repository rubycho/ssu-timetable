# test.py: prints every classes
from timetable.parser import Parser, ParserActions

parser = Parser()
parser.action(ParserActions.INIT, 0)


def print_data():
    parser.action(ParserActions.SEARCH, None)
    table = parser.get_data(ParserActions.SEARCH)

    length = 0
    if table:
        for td in table.find_all('tr'):
            if len(td.find_all('td')) < 2:
                continue
            print(td.text)
            length += 1

        print('Total: ', end='')
        print(length)


print("YEAR SELECTIONS:")
print(parser.get_selection(ParserActions.YEAR))
print("SEMESTER SELECTIONS:")
print(parser.get_selection(ParserActions.SEMESTER))

parser.action(ParserActions.YEAR, '2018')
parser.action(ParserActions.SEMESTER, '092')

for tab_selection in parser.get_selection(ParserActions.TAB):
    parser.action(ParserActions.TAB, tab_selection[0])

    out_of_range = False

    sel1 = parser.get_selection(ParserActions.SEL1)
    if len(sel1) is not 0:
        for sel1_selection in sel1:
            parser.action(ParserActions.SEL1, sel1_selection[0])
            sel2 = parser.get_selection(ParserActions.SEL2)
            if len(sel2) is not 0:
                for sel2_selection in sel2:
                    parser.action(ParserActions.SEL2, sel2_selection[0])
                    sel3 = parser.get_selection(ParserActions.SEL3)
                    if len(sel3) is not 0:
                        for sel3_selection in sel3:
                            parser.action(ParserActions.SEL3, sel3_selection[0])
                            print_data()
                    else:
                        print_data()
            else:
                print_data()
    else:
        print_data()
