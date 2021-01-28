Payment Process Flask Web Api Challenge
=======================================

Task Description
----------------

Write a Flask Web API with only 1 method called “ProcessPayment” that receives a request
like this
- CreditCardNumber (mandatory, string, it should be a valid credit card number)
- CardHolder: (mandatory, string)
- ExpirationDate (mandatory, DateTime, it cannot be in the past)
- SecurityCode (optional, string, 3 digits)
- Amount (mandatoy decimal, positive amount)

The response of this method should be 1 of the followings based on
- Payment is processed: 200 OK
- The request is invalid: 400 bad request
- Any error: 500 internal server error

The payment could be processed using different payment providers (external services)
called:
- PremiumPaymentGateway
- ExpensivePaymentGateway
- CheapPaymentGateway.

The payment gateway that should be used to process each payment follows the next set of
business rules:
a) If the amount to be paid is less than £20, use CheapPaymentGateway.
b) If the amount to be paid is £21-500, use ExpensivePaymentGateway if available.
Otherwise, retry only once with CheapPaymentGateway.
c) If the amount is > £500, try only PremiumPaymentGateway and retry up to 3 times
in case payment does not get processed.

Recommandations
---------------
- The classes should be written in such way that they are easy to test.
- Write as many tests as you think is enough to be certain about your solution works - Use SOLID principles.
- Decouple the logic the prediction logic from the API as much as possible

Installation
------------

follow the installation guides below.

### Installation in Windows

* Download and install [Python
  3.6.x](https://www.python.org/downloads/windows).  For this
  guide, we assume Python is installed in `C:\Python35`.
* Download the Pip (Python package installer) bootstrap script
  [get-pip.py](https://bootstrap.pypa.io/get-pip.py).
* In the command prompt, run `C:\Python36\python.exe get-pip.py` to install
  `pip`.
* In the command prompt, run `C:\Python36\scripts\pip install virtualenv` to
  install `virtualenv`.
  
* Download and Install postgresql 12 (https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

### Installation in Ubuntu

Python 3 is preinstalled in Ubuntu. Virtualenv and pip necessarily aren't, so:

* `sudo apt-get install python-virtualenv python-pip`

Install postgresql 12 (https://www.postgresql.org/download/linux/ubuntu/)

* Create the file repository configuration:
`sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'`

* Import the repository signing key:
`wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - `

* Update the package lists:
`sudo apt-get update`

* Install the latest version of PostgreSQL.
`sudo apt-get -y install postgresql-12`

### Creating and activating a virtualenv

Go to the project root directory and run:

Windows:

```
c:\location_of_project>C:\Python36\python.exe -m venv ./venv
c:\location_of_project>venv\Scripts\activate
```

Ubuntu:

```
virtualenv -p /usr/bin/python3 --system-site-packages venv
source venv/bin/activate
```

Required
--------

Connect to postgresql and create emty database

`CREATE DATABASE flask_app`


Configure the project
---------------------

Enter information for the databse

```
cd PaymentProcess/flask_app
nano config.py
```

Starting the project
--------------------

After activating the virtualenv do the following

```
cd PaymentProcess
pip install -r requirements.txt
cd flask_app
```
### in Ubuntu

`export FLASK_APP=app.py`


### in Windows

`set FLASK_APP=app.py`

```
flask db upgrade
flask run
```

Initialyse Table paymentType in Database
----------------------------------------
```
* cd PaymentProcess
* psql -h hostname -p port -U username database -f data.sql
```

Where :
   - hostname : host of database
   - port : port to connect on database
   - username : username of the databse owner




Now the test should be visible in the browser at
[`http://127.0.0.1:5000/swagger/`](http://127.0.0.1:5000/swagger/).

