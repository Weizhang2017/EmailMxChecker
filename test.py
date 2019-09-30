from smtplib import SMTP
# from logger import Logger
from EmailMxChecker import SMTPHandshake, CheckMx, EmailValidator
import dns.resolver
import csv

def main():
	with SMTP(host='aspmx.l.google.com.', port=0, local_hostname='asd.com') as smtp:
		logger.debug(smtp.helo(name='asd.com'))
		logger.debug(smtp.mail('asd@asd.com'))
		logger.debug(smtp.rcpt('test@gmail.com'))
		# logger.debug(smtp.verify('wzhang@leadbook.com'))
		logger.debug(smtp.quit())

def test_handshake():
	res = SMTPVerification.verify('test@gmail.com', 
		'aspmx.l.google.com', 
		'asd@asd.com', 
		'asd.com')
	logger.debug(res)

def test_verify():
	logger_test = Logger()
	smtphandshake = SMTPHandshake(
		rcpt_to_address='test@gmail.com', 
		mx='aspmx.l.googlsde.com', 
		fqdn='asd.com'
		)
	logger_test.debug(smtphandshake.verify())

def test_search_mx():
	try:
		answers = dns.resolver.query('achivecone.site', 'MX')
		for rdata in answers:
			print('Host', rdata.exchange, 'has preference', rdata.preference)
	except dns.resolver.NXDOMAIN as e:
		print(f'{e}')
	except dns.resolver.NoAnswer as mxerr:
		print(f'{mxerr}')

def test_CheckMx():
	check_mx = CheckMx('gmail.com')
	check_mx.first_mx()
	print('+'*128)
	mx = check_mx.list_mx()
	print(mx)

def test_emailvalidator():
	email_validator = EmailValidator('asd.com')
	result1 = email_validator.validate('rong.liu@rdbio.com')
	# print(result1)
	# result2 = email_validator.validate('test123@gmail.com')
	# print(result2)
	# result3 = email_validator.validate('test@hotmail.com')
	# print(result3)

def error_email_address():
	email_validator = EmailValidator('asd.com')
	with open('invalid_email_test.txt', 'r') as f:
		reader = csv.reader(f)
		with open('res_invalid_email_test.txt', 'w') as f2:
			for line in list(reader)[1:]:
				result_cat = email_validator.check_catchall(line[0])
				if not result_cat:
					result = email_validator.validate(line[0])
				else:
					result = 'catch_all_domain'
				f2.write(f'{line[0]}, {result}\n')
if __name__ == '__main__':
	# test_CheckMx()
	error_email_address()
	