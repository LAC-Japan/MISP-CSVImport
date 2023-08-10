# Copyright (c) 2018 LAC Co.,Ltd.
# All rights reserved.
#
# This software is released under the BSD License.
# https://opensource.org/licenses/BSD-2-Clause

import argparse
import pathlib
import traceback
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
from InputFileParser import InputFileParser
from MISPController import MISPController
import const


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, dest='input_file',
                        help='input file', type=pathlib.Path)
    parser.add_argument('--skip-header', action='store_true', default=False,
                        dest='skip_header', help='Skip header flag(default False)')
    parser.add_argument('--cs', default='\t',
                        dest='column_separator', help='Column separator')
    parser.add_argument('--ls', default='\n',
                        dest='line_separator', help='Line separator')
    parser.add_argument('--target-row', default=1,
                        dest='target_row', help='Target row number', type=int)
    args = parser.parse_args()

    print('Import file parsing')
    file_parser = InputFileParser(separator=args.column_separator, line_separator=args.line_separator,
                                  skip_header=args.skip_header, target_row=args.target_row)
    import_events = file_parser.parse(args.input_file)
    if len(import_events) == 0:
        print('no import event')
        exit(0)

    import_events.sort(key=lambda x: x['user'])

    print('Import MISP start')
    controllers = {}
    for user, import_config in const.IMPORT_CONFIG.items():
        controllers[user] = MISPController({
            'url': const.MISP_URL, 'authkey': import_config['authkey'], 'distribution': import_config['distribution'], 'threat_level_id': import_config['threat_level'], 'analysis': import_config['analysis_level'], 'max_retry_count': 5
        })

    exist_error = False
    for event in import_events:
        if event['user'] not in controllers:
            exist_error = True
            print('No exist authkey: {}'.format(event['user']))

    if exist_error:
        exit(1)

    for event in import_events:
        try:
            controllers[event['user']].import_event(event)
        except:
            print('import event failed')
            print(event)
            print(traceback.format_exc())

    print('All done')
