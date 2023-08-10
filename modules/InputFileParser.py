# Copyright (c) 2018 LAC Co.,Ltd.
# All rights reserved.
#
# This software is released under the BSD License.
# https://opensource.org/licenses/BSD-2-Clause

import pathlib
import csv
import os


class InputFileParser(object):
    ''' Input file parser '''

    # define input file columns
    FILE_COLUMNS = {
        'date': 0, 'orgg': 1, 'user': 2, 'title': 3, 'tag1': 4, 'tag2': 5, 'tag3': 6, 'tag4': 7, 'value': 8, 'category': 9, 'type': 10, 'attribute_tags': 11, 'comment': 12
    }

    def __init__(self, separator='\t', line_separator='\n', skip_header=False, charset='utf-8', target_row=1):
        self.separator = separator
        self.line_separator = line_separator
        self.skip_header = skip_header
        self.charset = charset
        self.target_row = target_row

    def parse(self, inputfile):
        ''' Parses the input file.
                imputfile: input file
                return: dict data
        '''

        results = {}

        csv_values = self._parse_csvfile(
            inputfile, self.separator, self.line_separator, self.FILE_COLUMNS, self.target_row)
        if csv_values == None:
            return []

        for line, values in csv_values.items():

            event_title = values['title'].strip()
            if len(event_title) == 0:
                print('Unset event title\n{}'.format(line))
                return []

            if event_title in results:
                event_data = results[event_title]
            else:
                event_data = {
                    'user': values['user'], 'title': event_title, 'date': values['date'], 'event_tags': [], 'attributes': []
                }

            event_tags = event_data['event_tags']
            attributes = event_data['attributes']

            # add tags
            self._add_tags(event_tags, values['tag1'])
            self._add_tags(event_tags, values['tag2'])
            self._add_tags(event_tags, values['tag3'])
            self._add_tags(event_tags, values['tag4'])
            attribute_tags = []
            self._add_tags(attribute_tags, values['attribute_tags'])

            # add attributes
            attribute = {
                'value': values['value'].strip(), 'category': values['category'].strip(), 'type': values['type'].strip(), 'comment': values['comment'].strip(), 'tags': attribute_tags
            }

            self._add_attribute(attributes, attribute)

            event_data['event_tags'] = event_tags
            event_data['attributes'] = attributes
            results[event_title] = event_data

        return list(results.values())

    @staticmethod
    def _add_attribute(attributes, target_attribute):

        for attribute in attributes:

            if attribute['type'] == target_attribute['type'] and attribute['category'] == target_attribute['category'] and attribute['value'] == target_attribute['value']:
                print('Duplicate attribute(type/category/value)')
                print(target_attribute)
                return

        attributes.append(target_attribute)

    def _parse_csvfile(self, csv_file, separator, line_separator, columns, target_row):
        ''' Parse the CSV file and return the result
                csv_file: target file
                separator: separator
                line_separator: line separator
                columns: Column information (dict whose name is the key index)
                target_row: import target row number
        '''

        results = {}

        if target_row > 1:
            print('Skip to the row to be imported(target row: {})'.format(target_row))

        try:

            with csv_file.open('r', encoding=self.charset) as infile:
                csvFile = csv.reader(
                    infile, delimiter=separator, lineterminator=line_separator, dialect='excel')

                row_cnt = 0
                for values in csvFile:
                    row_cnt = row_cnt + 1

                    if row_cnt < target_row:
                        continue

                    if self.skip_header and row_cnt == 1:
                        print('skip header')
                        continue

                    line = separator.join(values)

                    if len(values) != len(columns):
                        print('invalid format{}: {}'.format(
                            str(csv_file), line))
                        continue

                    result = {}
                    for itemName, index in columns.items():
                        result[itemName] = values[index]

                    results[line] = result

                return results

        except FileNotFoundError:
            print('file not found: {}'.format(str(csv_file)))
        return None

    @staticmethod
    def _add_tags(target_list, tags):
        ''' Add a tag. There is a possibility that tag can be divided by ,
                target_list: target list
                tags: add strings
        '''

        if len(tags) == 0:
            return

        for tag in tags.split(','):

            if tag.strip() not in target_list:
                target_list.append(tag.strip())
