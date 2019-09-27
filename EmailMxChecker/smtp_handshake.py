import smtplib
import random
import string
import re
from .logger import Logger
import socket

logger = Logger(name='smtp_handshake')

class SMTPHandshake:
    '''
    Validate email address by SMTP handshake
    key arguments:
        rcpt_to_address: 
            the email address to be verified.
        mx:
            mx server for the email address to be verified.
        fqdn:
            fully qualified domain name. A domain name for the system runing 
            this programm. The targeted email server may check fqdn of the system,
            if not found or invalid, connection may be refused.
        mail_from_address:
            optional. If not specified, the program will generate a random
            email ID with the fqdn.
    '''

    email_pattern = r'^[0-9a-zA-Z][0-9a-zA-Z_\-\.]*[0-9a-zA-Z]@[0-9a-zA-Z][0-9a-zA-Z\.-]*[a-zA-Z]$'
    fqdn_pattern = r'[\w]*.[\w]*'

    def __init__(self, *, rcpt_to_address, mx, fqdn, mail_from_address=None):
        self.rcpt_to_address = rcpt_to_address
        self.mx = mx
        self.fqdn = fqdn
        self.mail_from_address = mail_from_address

    @property
    def rcpt_to_address(self):
        return self._rcpt_to_address

    @property
    def mx(self):
        return self._mx

    @property
    def mail_from_address(self):
        return self._mail_from_address

    @property
    def fqdn(self):
        return self._fqdn

    @fqdn.setter
    def fqdn(self, value):
        if re.search(self.fqdn_pattern, value) is None:
            raise ValueError('Invalid FQDN format')
        self._fqdn = value
    
    
    @mail_from_address.setter
    def mail_from_address(self, value):
        if value is None:
            self._mail_from_address = self.__class__.random_email(self.fqdn)
        elif re.search(self.email_pattern, value) is None:
            raise ValueError('Invalid Email address format')
        
    
    @mx.setter
    def mx(self, value):
         self._mx = value

    @rcpt_to_address.setter
    def rcpt_to_address(self, value):
        if re.search(self.email_pattern, value) is None:
            raise ValueError('Invalid Email address format')
        self._rcpt_to_address = value
    

    def verify(self):
        '''Verifiy email address by SMTP handshake'''

        code, message = self.__class__.smtp_handshake(
            self.rcpt_to_address, self.mx, self.fqdn, self.mail_from_address
            )
        result = self.__class__.result_paser(code)
        logger.info(f'email address:{self.rcpt_to_address}, result: {code}, {message}')
        return result

    @staticmethod
    def smtp_handshake(rcpt_to_address, mx, fqdn, mail_from_address):
        """
        Performs smtp handshake to recipient email server and try to verify the email address.
        """
        code, msg = 0, None
        try:
            server = smtplib.SMTP(local_hostname=fqdn, timeout=10)
            server.connect(mx)
            server.ehlo(name=fqdn)
            server.mail(mail_from_address)
            code, msg = server.rcpt(rcpt_to_address)
            msg = "".join(map(chr, msg))
            server.quit()
        except smtplib.SMTPServerDisconnected as err:
            msg = str("SMTP Server don't allow ping: ".format(err))
            code = -1
        except socket.timeout as serr:
            msg = "Unable to connect to SMTP server"
            code = -1
        except socket.error as eerr:
            msg = "Socket exception"
            code = -1
        except smtplib.SMTPException as e:
            msg = str(e)
            code = -1
        except AttributeError as aerr:
            msg = msg
        return code, msg

    @staticmethod
    def random_email(domain):
        '''Generate a random email address with a given domain'''
        randon_string =  ''.join(random.choice(string.ascii_lowercase) 
            for _ in range(7)) 
        return f'{randon_string}@{domain}'

    @staticmethod
    def result_paser(code):
        '''
        Parse the code and messages and return the validity 
        of the email address
        code: 
        '''
        if code == -1:
            return Result.CONNECTIONTIMEOUT
        elif code == 250:
            return Result.ACCEPTED
        else:
            return Result.REJECTED


class Result:
    '''Results from SMTP handshake'''
    CONNECTIONTIMEOUT = 'mx connection timeout'
    REJECTED = 'email address rejected'
    ACCEPTED = 'email address accepted'
