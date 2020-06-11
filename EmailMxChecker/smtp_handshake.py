import smtplib
import random
import string
import re
from .logger import Logger
import socket
import logging

logger = Logger(name=__name__, level=logging.WARNING,
     handlers=['stream', 'file'], filename='mx_unknown_response.log')

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
    _response_type = ['short', 'long']

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
        else:
            self._mail_from_address = value
        
    
    @mx.setter
    def mx(self, value):
         self._mx = value

    @rcpt_to_address.setter
    def rcpt_to_address(self, value):
        if re.search(self.email_pattern, value) is None:
            raise ValueError('Invalid Email address format')
        self._rcpt_to_address = value
    

    def verify(self, response_type='short'):
        '''
        Verifiy email address by SMTP handshake
        if response_type == "short", return interpreted result only
        if response_type == "long", return interpreted result and raw message
        '''

        if response_type not in self._response_type:
            raise ValueError(f'Invalid response type. Expected of of {_response_type}')

        code, message = self.__class__.smtp_handshake(
            self.rcpt_to_address, self.mx, self.fqdn, self.mail_from_address
            )
        result = self.__class__.result_paser(code, message)
        if result == Result.UNKNOWN:
            logger.warning(f'email address:{self.rcpt_to_address}, result: {code}, {message}')
        else:
            logger.info(f'email address:{self.rcpt_to_address}, result: {code}, {message}')
        if response_type == 'short':
            return result
        elif response_type == 'long':
            return result, message

    @staticmethod
    def smtp_handshake(rcpt_to_address, mx, fqdn, mail_from_address):
        """
        Performs smtp handshake to recipient email server and try to verify the email address.
        """
        code, msg = 0, None
        try:
            server = smtplib.SMTP(local_hostname=fqdn, timeout=8)
            server.connect(mx)
            server.ehlo(name=fqdn)
            server.mail(mail_from_address)
            code, msg = server.rcpt(rcpt_to_address)
            msg = "".join(map(chr, msg))
            server.quit()
        except smtplib.SMTPServerDisconnected as err:
            msg = str("SMTP Server doesn't allow ping: {}".format(err))
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
    def result_paser(code, message):
        '''
        Parse the code and messages and return the validity 
        of the email address
        code: 
        '''
        if code == -1:
            return Result.CONNECTION_ERR
        elif code == 250:
            return Result.ACCEPTED
        elif code == 503:
            return Result.ACCESS_DENIED
        elif code == 454 or code == 551 or\
            re.search(Pattern.INVALID_RECIPIENT, message, re.IGNORECASE):
            return Result.INVALID_RECIPIENT
        elif re.search(Pattern.BLOCKED, message, re.IGNORECASE):
            return Result.BLOCKED
        elif re.search(Pattern.REVERSE_DNS, message, re.IGNORECASE):
            return Result.REVERSE_DNS
        elif re.search(Pattern.GREYLISTING, message, re.IGNORECASE):
            return Result.GREYLISTING
        else:
            return Result.UNKNOWN


class Result:
    '''Results from SMTP handshake'''
    CONNECTION_ERR = 'mx_connection_error'
    INVALID_RECIPIENT = 'invalid_recipient'
    ACCEPTED = 'email_address_accepted'
    ACCESS_DENIED = 'mx_server_access_denied'
    BLOCKED = 'access blocked'
    REVERSE_DNS = 'mx_server_access_denied: reserse DNS'
    UNKNOWN = 'unknown_response'
    GREYLISTING = 'greylisted'

class Pattern:
    BLOCKED = r'block|blacklist'
    REVERSE_DNS = r'reverse'
    INVALID_RECIPIENT = (r'address\s*rejected|invalid\s*recipient|no\s*mailbox|not\s*exist|'
                        r'unknown|unavailable|not.*found|no longer accept|no.*users')
    GREYLISTING = r'internal resource temporarily unavailable|greylist'
