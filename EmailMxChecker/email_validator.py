from .smtp_handshake import SMTPHandshake, Result
from .mx_checker import CheckMx

class EmailValidator(SMTPHandshake, CheckMx):
	'''
	Validate mx domain and email address
	arguments:
		fqdn: 
			fully qualified domain name. A domain name for the system runing 
			this programm. The targeted email server may check fqdn of the system,
			if not found or invalid, connection may be refused.
		mail_from_address:
			optional. If not specified, the program will generate a random
			email ID with the fqdn.
	'''

	email_pattern = r'^[0-9a-zA-Z][0-9a-zA-Z_\-\.]*[0-9a-zA-Z]@[0-9a-zA-Z][0-9a-zA-Z\.-]*[a-zA-Z]$'

	def __init__(self, fqdn, mail_from_address=None):
		self.fqdn = fqdn
		self.mail_from_address = mail_from_address
		
  
	def _get_domain(self, domain):
		'''
		Find the mx domain with the highest priority
		'''
		CheckMx.__init__(self, domain)
		mx_domain, _ = self.first_mx()
		return mx_domain

	def validate(self, email_address,response_type='short'):
		'''
		Validate an email address
		return: mx connection timeout
				email address rejected
				email address accepted
				domain not found
		'''

		domain = email_address.split('@')[-1]

		mx_domain = self._get_domain(domain)
		if mx_domain:
			SMTPHandshake.__init__(
				self,
				rcpt_to_address=email_address,
				mx=mx_domain,
				fqdn=self.fqdn,
				mail_from_address=self.mail_from_address
				)
			result = self.verify(response_type)
		else:
			result = 'domain not found'
		return result

	def check_catchall(self, email_address):
		'''
		Check whether an mx is catchall
		return: CATCHALL 1
				NON CATCHALL 0
		'''
		domain = email_address.split('@')[-1]
		mx_domain = self._get_domain(domain)
		if mx_domain:
			random_rcpt_address = self.__class__.random_email(domain)
			SMTPHandshake.__init__(
				self,
				rcpt_to_address=random_rcpt_address,
				mx=mx_domain,
				fqdn=self.fqdn,
				mail_from_address=self.mail_from_address
				)
			result = self.verify()
			if result == Result.ACCEPTED:
				IS_CATCHALL = 1
			else:
				IS_CATCHALL = 0	
		else:
			IS_CATCHALL = -1

		return IS_CATCHALL
