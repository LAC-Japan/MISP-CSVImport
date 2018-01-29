import time, datetime, traceback
from pymisp import PyMISP, MISPEvent, MISPAttribute

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

class MISPController(object):
	''' MISP Controller '''

	def __init__(self, misp_param, debug = False):
		self.misp_param = misp_param
		self.debug = debug

		if misp_param.get('connect_immediately', False):
			self._connect()
		else:
			self.misp = None

	def import_event(self, event_data):
		''' Import event '''

		# Check registered same event info
		print('importing: {}'.format(event_data['title']))
		events = self._search_event(eventinfo = event_data['title'])
		if events != None:
			for event in events:
				if event_data['title'] == event['Event']['info']:
					self._remove_event(event['Event']['id'])

		event = self._add_event(event_data)
		if event:
			print('created event: {}'.format(event.id))
		else:
			print("Import failed.Please retry: {}".format(event_data['title']))

	def _connect(self):
		self.debug_print('URL: {}'.format(self.misp_param['url']))
		self.debug_print('apikey: {}'.format(self.misp_param['apikey']))
		self.misp = PyMISP(self.misp_param['url'], self.misp_param['apikey'], False, 'json')
		self._registered_tags = self.misp.get_all_tags()

	def _check_tag(self, target_tag):

		if self.misp == None:
			self._connect()

		for tag_info in self._registered_tags.get('Tag', {}):
			if tag_info.get('name', '') == target_tag:
				return True

		self.debug_print('new tag: {}'.format(target_tag))

		cnt = 0
		while True:
			try:
				if self.misp == None:
					self._connect()

				self.misp.new_tag(target_tag, exportable = True)
				self._registered_tags = self.misp.get_all_tags()
				return True

			except:
				print(traceback.format_exc())

				if cnt < int(self.misp_param.get('max_retry_count', '0')):
					print('add new tag retry: {}'.format(cnt))
					cnt = cnt + 1
					time.sleep(10)
				else:
					return False

	def _add_event(self, value):

		for tag in value['event_tags']:
			self._check_tag(tag)

		for attribute in value['attributes']:
			for tag in attribute['tags']:
				self._check_tag(tag)

		cnt = 0
		while True:
			try:

				if self.misp == None:
					self._connect()

				response = self.misp.new_event(
					self.misp_param['distribution']
					,self.misp_param['threat_level_id']
					,self.misp_param['analysis']
					, value['title']
					, date = value['date']
					, published=True
				)
				if response.get('errors'):
					raise Exception(str(response['errors']))

				event = MISPEvent()
				event.load(response)
				break

			except:
				print(traceback.format_exc())

				if cnt < int(self.misp_param.get('max_retry_count', '0')):
					print('add new event retry: {}'.format(cnt))
					cnt = cnt + 1
					time.sleep(10)
				else:
					return None

		self.debug_print(event.id)

		for tag in value['event_tags']:
				event.add_tag(tag)

		for attribute in value['attributes']:
			attribute_tags = []

			event.add_attribute(
				type = attribute['type']
				, value = attribute['value']
				, category = attribute['category']
				, comment = attribute.get('comment', '')
				, distribution = self.misp_param['distribution']
				, Tag = self._create_tags(attribute['tags'])
			)

		if self._update_event(event):
			self.debug_print('completed')
			return event
		else:
			self.debug_print('add failed')
			return None

	def _get_event(self, id):

		cnt = 0
		while True:
			try:
				if self.misp == None:
					self._connect()

				self.debug_print('get event start: {}'.format(id))
				event=self.misp.get_event(id)
				if event.get('errors'):
					raise Exception(str(event['errors']))

				self.debug_print('get event end: {}'.format(id))

				return event

			except:
				print(traceback.format_exc())

				if cnt < int(self.misp_param.get('max_retry_count', '0')):
					print('get event retry: {}'.format(cnt))
					cnt = cnt + 1
					time.sleep(10)
				else:
					return None

	def _remove_event(self, id):

		if id:
			print('delete event: {}'.format(id))
			cnt = 0
			while True:
				try:
					if self.misp == None:
						self._connect()

					response = self.misp.delete_event(id)
					if response.get('errors'):
						raise Exception(str(response['errors']))

					return True

				except:
					print(traceback.format_exc())

					if cnt < int(self.misp_param.get('max_retry_count', '0')):
						print('remove event retry: {}'.format(cnt))
						cnt = cnt + 1
						time.sleep(10)
					else:
						return False

	def _search_event(self, **cons):

		cnt = 0
		while True:
			try:
				if self.misp == None:
					self._connect()

				self.debug_print('search event start')
				response = self.misp.search_index(**cons)
				if response.get('errors'):
					raise Exception(str(response['errors']))

				results = []
				self.debug_print('search event end')

				for json in response.get('response', []):

					if json.get('id', ''):
						results.append(self._get_event(json['id']))
					else:
						print('no event ID')
						print(json)

				return results

			except:
				print(traceback.format_exc())

				if cnt < int(self.misp_param.get('max_retry_count', '0')):
					print('search event retry: {}'.format(cnt))
					cnt = cnt + 1
					time.sleep(10)
				else:
					return None

	def _update_event(self, event):
		cnt = 0

		while True:
			try:
				if self.misp == None:
					self._connect()

				self.debug_print('event update start: {}'.format(event.id))
				response = self.misp.update(event)
				if response.get('errors'):
					raise Exception(str(response['errors']))

				self.debug_print('{} updated'.format(event.id))
				return True

			except:
				print(traceback.format_exc())

				if cnt < int(self.misp_param.get('max_retry_count', '0')):
					print('retry: {}'.format(cnt))
					cnt = cnt + 1
					time.sleep(10)
				else:
					print('event update failed: {}'.format(event.info))
					try:
						self._remove_event(event.id)
					except:
						pass
					return False

	def _create_tags(self, values):
		tags=[]

		for value in values:
			if value:
				tags.append({'name': value})

		return tags

	def debug_print(self, message):
		if self.debug == False:
			return
#		nowstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		nowstr = datetime.datetime.now().strftime('%H:%M:%S')

		print('{}\t{}'.format(nowstr, message))
