### A module to verify email address

#### Installation

Install using pip:
```shell
pip install EmailMxChecker
```
Install from Github:
```shell
git clone https://github.com/Weizhang2017/EmailMxChecker
cd EmailMxChecker 
python setup.py install
```


###### Simple Examples:

Check an MX server associated with a domain
```python
from EmailMxChecker import CheckMx

check_mx = CheckMx('google.com')

mx = check_mx.list_mx()
```

Verify an email address
```python
from EmailMxChecker import EmailValidator

email_validator = EmailValidator('abc.com')
result = email_validator.validate('wrong_email_id@gmail.com')
```

###### v1.1.10 update
Return mx response by specifying argument response_type
```python
result = email_validator.validate('wrong_email_id@gmail.com', response_type='long')
>>>print(result)
('invalid_recipient', "5.1.1 The email account that you tried to reach does not exist. \
Please try\n5.1.1 double-checking the recipient's email address for typos or\n5.1.1 unnecessary \
spaces. Learn more at\n5.1.1  https://support.google.com/mail/?p=NoSuchUser q36si1115197pjq.147 - gsmtp")
```


