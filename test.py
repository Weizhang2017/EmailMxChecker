from smtplib import SMTP
from EmailMxChecker.logger import Logger
from EmailMxChecker import SMTPHandshake, CheckMx, EmailValidator
import dns.resolver
import csv
logger = Logger(__name__)

def main():
	with SMTP(host='aspmx.l.google.com.', port=0, local_hostname='asd.com') as smtp:
		logger.debug(smtp.helo(name='asd.com'))
		logger.debug(smtp.mail('asd@asd.com'))
		logger.debug(smtp.rcpt('test@gmail.com'))
		# logger.debug(smtp.verify('wzhang@leadbook.com'))
		logger.debug(smtp.quit())

def test_handshake():
	smtp_handshake = SMTPHandshake(
		rcpt_to_address='zha21ngw1.2011@gmail.com', 
		mx='gmail-smtp-in.l.google.com', 
		fqdn='asd.com',
		# mail_from_address='asd@asd.com'
		)
	logger.debug(smtp_handshake.verify(response_type='long'))

def test_verify():
	smtphandshake = SMTPHandshake(
		rcpt_to_address='zhangw1.2011@gmail.com', 
		mx='aspmx.l.google.com', 
		fqdn='asd.com'
		)
	logger.debug(smtphandshake.verify(response_type='long'))

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
	check_mx = CheckMx('gmail1323.com')
	check_mx.first_mx()
	print('+'*128)
	mx = check_mx.list_mx()
	print(mx)

def test_emailvalidator():
	email_validator = EmailValidator('asd.com')
	result1 = email_validator.validate('wrong_email_id@gmail.com', response_type='long')
	print(result1)
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

def socket_err_test():
	email_validator = EmailValidator('asd.com')
	result1 = email_validator.validate('jyotiranjan.patra@bharti-axagi.co.in', response_type='long')
	print(result1)

def socket_err_catchall_test():
	email_validator = EmailValidator('asd.com')
	result1 = email_validator.check_catchall('jyotiranjan.patra@bharti-axagi.co.in')
	print(result1)

if __name__ == '__main__':
	# test_CheckMx()
	# error_email_address()
	socket_err_catchall_test()