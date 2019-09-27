### A wrapper for [kafka-python](https://kafka-python.readthedocs.io/en/master/usage.html)

#### Installation

Install using pip:
```shell
pip install EmailMxChecker
```
Install from Github:
```shell
git clone https://github.com/Weizhang2017/EmailMxChecker
cd pythonKakfaWrapper 
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
