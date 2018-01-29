# Import MISP Event from file script
# Copyright (c) 2018 LAC Co.,Ltd. All rights reserved.

import argparse
import pathlib
import traceback

import const
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from InputFileParser import InputFileParser
from MISPController import MISPController

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', required=True, dest='input_file', help='input file', type=pathlib.Path)
	parser.add_argument('--skip-header', action='store_true', default = False, dest='skip_header', help='Skip header flag(default False)')
	parser.add_argument('--cs', default = '\t', dest='column_separator', help='Column separator')
	parser.add_argument('--ls', default = '\n', dest='line_separator', help='Line separator')
	parser.add_argument('--target-row', default = 1, dest='target_row', help='Target row number', type=int)
	args = parser.parse_args()

	print('Import file parsing')
	file_parser = InputFileParser(separator = args.column_separator, line_separator = args.line_separator, skip_header = args.skip_header, target_row=args.target_row)
	import_events = file_parser.parse(args.input_file)
	if len(import_events) == 0:
		print('no import event')
		exit(0)

	import_events.sort(key=lambda x: x['user'])

	print('Import MISP start')
	controllers = {}
	for user, apikey in const.MISP_APIKEYS.items():
		controllers[user] = MISPController({
			'url': const.MISP_URL
			, 'apikey': apikey
			, 'distribution': const.DISTRIBUTION
			, 'threat_level_id': const.THREAT_LEVEL
			, 'analysis': const.ANALYSIS_LEVEL
			, 'max_retry_count': 5
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
