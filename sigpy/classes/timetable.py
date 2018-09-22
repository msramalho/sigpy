import re
from lxml.html import fromstring  # , HtmlElement
from lxml.etree import tostring
from collections import defaultdict
# from lxml.cssselect import CSSSelector as css
# from lxml import etree


class timetable:

    def __init__(self, html):
        self.tree = fromstring(html)

    # return the events in this timetable page
    def get_events(self):
        events = []
        table = self.tree.cssselect("table.horario")
        if len(table):
            self.table = table[0]
            matrix = self._parse_to_matrix(False, True)
            events = self._parse_events(matrix)
            events += self._parse_overlapping_events()
        return events

    # This converts the timetable into a matrix where ther is no rowspan and colspan
    # Events that stretch through more than one block are duplicated
    def _parse_to_matrix(self, dupCols=False, dupRows=False, textMode=False):
        columns = [None] * len(self.table.xpath("./tr/th"))  # every column is None
        curr_x = 0

        for row in self.table.xpath("./tr"):
            curr_y = 0
            for col in row.xpath("./td|./th"):
                rowspan = int(col.get("rowspan", 1))
                colspan = int(col.get("colspan", 1))
                content = ''.join([str(tostring(c, encoding="unicode")) for c in col.iterchildren()])
                content = col.text if not len(content) else content
                content = content.replace(u'\xa0', u' ').strip()

                for x in range(rowspan):
                    for y in range(colspan):

                        if not columns[curr_y + y]:
                            columns[curr_y + y] = [None] * 50

                        while columns[curr_y + y][curr_x + x]:
                            curr_y += 1
                            if not columns[curr_y + y]:
                                columns[curr_y + y] = [None] * 50

                        if (x == 0 or dupRows) and (y == 0 or dupCols):
                            columns[curr_y + y][curr_x + x] = content
                        else:
                            columns[curr_y + y][curr_x + x] = ""
                curr_y += 1
            curr_x += 1
        return columns

    def _parse_events(self, matrix):
        events = []
        for i in range(1, len(matrix)):  # iterate over the table columns
            day = matrix[i]
            counter = 1  # count the number of blocks this class takes
            for j in range(2, len(day)):  # ignore the first row with day names, start at two to see previous
                # if this event stops toDay and is not empty or
                # if its the last event of the day and is not empty
                if (day[j] != day[j - 1] or j == len(day) - 1) and (day[j - 1] is not None and len(day[j - 1]) > 0):
                    events.append(timetable._get_event(day[j - 1], i, matrix[0][j - counter], matrix[0][j - 1]))
                    counter = 1
                elif day[j] == day[j - 1]:
                    counter += 1
                elif day[j] != day[j - 1]:
                    counter = 1
        return events

    # receives a <td> element and extracts all the info in a dict
    def _get_event(html, day, start, end):
        tree = fromstring("<div>%s</div>" % html)
        class_a = tree.cssselect("span.textopequenoc a")[0]
        room_td = tree.cssselect("table.formatar td")[0]
        teacher_a = tree.cssselect("table.formatar td.textod")[0].cssselect("a")[0]

        return {
            "from": start,
            "to": end,
            "day": day,
            "name": tree.cssselect("b acronym")[0].get("title", ""),
            "acronym": tree.cssselect("b a")[0].text,
            "type": re.findall('\((.+)\)', tree.xpath(".//b/text()")[0])[0],
            "class": {
                "name": class_a.text,
                "url": class_a.cssselect("a")[0].get("href", "")
            },
            "room": {
                "name": room_td.text,
                "url": room_td.cssselect("a")[0].get("href", ""),
            },
            "teacher": {
                "name": teacher_a.get("title", ""),
                "acronym": teacher_a.text,
                "url": teacher_a.get("href", ""),
            }
        }

    # extracts overlapping events from a timetable page
    def _parse_overlapping_events(self):
        events = []
        for o in self.tree.cssselect("table.dados tr.d"):
            events.append(self._get_overlapping_event(o))
        return events

    # parse and get a dict with all the info for an overlapping class
    def _get_overlapping_event(self, tree):
        class_a = tree.cssselect('[headers="t6"] a')[0]
        room_a = tree.cssselect('[headers="t4"] a')[0]
        teacher_a = tree.cssselect('[headers="t5"] a')[0]

        return {
            "from": tree.cssselect('[headers="t3"]')[0].text,
            "to": None,  # unable to retrive from this table
            "day": tree.cssselect('[headers="t2"]')[0].text,
            "name": tree.cssselect('[headers="t1"] acronym')[0].get("title", ""),
            "acronym": tree.cssselect('[headers="t1"] a')[0].text,
            "type": re.findall('\((.+)\)', str(tostring(tree.cssselect('[headers="t1"]')[0])))[0],
            "class": {
                "name": class_a.text,
                "url": class_a.cssselect("a")[0].get("href", "")
            },
            "room": {
                "name": room_a.text,
                "url": room_a.cssselect("a")[0].get("href", ""),
            },
            "teacher": {
                # "name": teacher_a.get("title", ""),
                "acronym": teacher_a.text,
                "url": teacher_a.get("href", ""),
            }
        }
