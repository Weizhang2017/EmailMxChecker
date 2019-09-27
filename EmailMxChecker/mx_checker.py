import dns.resolver
import re
from .logger import Logger
logger = Logger(name='mx_checker')

class CheckMx:
	'''
	Check mx server for a given domain
	arguements:
		domain: the domain to check its mx server
	'''
	domain_pattern = r'^(?!:\/\/)([a-zA-Z0-9-_]+\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11}?$'

	def __init__(self, domain):
		self.domain = domain
		
	@property
	def domain(self):
		return self._domain
	
	@domain.setter
	def domain(self, value):
		if re.search(self.domain_pattern, value) is None:
			raise ValueError('Invalid domain format')
		else:
			self._domain = value

	def list_mx(self):
		'''
		Return all mx servers
		'''
		mx_list = list()
		code = 0
		try:
			answers = dns.resolver.query(self.domain, 'MX')
			for item in answers:
				mx_list.append((item.exchange, item.preference))
				logger.info(
					f'mx domain: {item.exchange} priority: {item.preference}'
					)
			code = 200
			
		except dns.resolver.NXDOMAIN as derr:
			logger.info('domain not found')
			code = 401

		except dns.resolver.NoAnswer as mxerr:
			logger.info('mx not found')
			code = 402

		return mx_list, code

	def first_mx(self):
		'''
		Return the mx domain with the highest priority
		'''
		priority = 100
		mx_domain = None
		try:
			answers = dns.resolver.query(self.domain, 'MX')
			for item in answers:
				if priority > item.preference:
					priority = item.preference
					mx_domain = item.exchange.to_text()
			logger.info(
				f'mx domain: {mx_domain} priority: {priority}'
				)

		except dns.resolver.NXDOMAIN as derr:
			logger.info('domain not found')
			code = 401

		except dns.resolver.NoAnswer as mxerr:
			logger.info('mx not found')
			code = 402

		return mx_domain, priority

