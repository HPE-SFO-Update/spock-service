# SFO_Update_Service setupfile

A Flask Service App

## Setup
### Requirements
[Install Python 3.6](https://www.python.org/downloads/release/python-360/)
[Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
[Python Virtual Environments](https://docs.python.org/3/library/venv.html)
[PyCharm](https://www.jetbrains.com/pycharm/)

Type the following in command shell:

	git clone git@github.com:HPE-SFO-Update/spock-service.git
	pip install -r requirements.txt


## Getting Started
### Run Flask Environment

How To Run Update Service App With HTTP

     python SFO_Update_Service.py --port 80

How To Run Update Service App With HTTPS

    python SFO_Update_Service.py --port 443  --cert './security/test_cert.pem' --key './security/test_key.pem'

