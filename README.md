# Home Automation and Security

The project automates your home appliances and electricity so that all the electric applicants can be controlled from anywhere from the world. This also concerns on security such as fire accident reporting etc.


The project mainly has three components:
1. Django (REST API).
2. ReactJS (front-end).
3. ESP board.
4. A bit of network configuration.

## Configuration

The configuration will be updated soon.

## Working

Let's deal all the four subcomponents in the project:

1. Django REST API

* Registration: <POST>





Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


Token based authentication is used here.

* Registration \
    url: `/accounts/create/` \
    request: 'POST' \
    parameters: 
    1. username
    2. password
    3. password-confirm
    4. email

Sample Curl request: 

```bash
 curl --request POST --header "Content-Type: application/json" --data '{"username": "sample", "password": "sample123", "password_confirm": "sample123", "email": "rammanoj@gmail.com"}' http://127.0.0.1:8000/accounts/create/
 ```
 
 * Mail verification can be done with the api
 `/accounts/mailverify/<unique_key>/`
 
 * Display User profile \
  url: `/accounts/<unique_id>/` \
  parameters: None \
  request: 'GET' \
  Parmaeters returned:
     1. Username
     2. email
 
 Sample Curl request: 
 ```bash
curl --request GET --header "Authorization: Token token_of_the_user" http://127.0.0.1:8000/accounts/number/
```

 * login \
    url: `/accounts/login/` \
    parameters: 
    1. username
    2. password
    request: 'POST' \
    parameters returned: 
    1. userid
    2. Token
    
Sample Curl request: 
```bash
curl --request POST --header "Content-Type: application/json" --data '{"username": "sample", "password": "sample123"}' http://127.0.0.1:8000/accounts/login/
```
    
 * logout \
  url: `accounts/logout/`
  request: 'POST'
  
Sample Curl request: 

```bash
curl --request POST --header "Content-Type: application/json" -H "Authorization: Token 172158ba5363e770c66188aba7048078009de537"  http://127.0.0.1:8000/accounts/logout/
```
 
 *  Password reset: \
    url: `accounts/forgot_password_reset/` \
    parameters: \
        1. email \
    request: 'POST' \
    example:
 ```bash
curl --request POST --header "Content-Type: application/json" --data '{"email": "sampleqweqweram@gmail.com"}' http://127.0.0.1:8000/accounts/forgot_password_reset/
``` 

*  Update Forgot Password \
    url: `accounts/forgot_password_update/<unique_link>/`
    request: 'PATCH' \
    parameters: 
    1. password
    2. confirm password
    
Sample Curl request:

```bash
curl --request PATCH --header "Content-Type: application/json" --data '{"password": "amma1234", "confirm_new": "amma1234"}' http://127.0.0.1:8000/accounts/forgot_password_update/f856bfeac4cbac828712cbd567fbd43f87875c3ce5d2c2320490dc485b7e84d0/
```

* Password change Operation
    url: `accounts/password_update/<user_id>` \
    request: 'PATCH' \
    parameters:
    1. password (new & old)
    
Sample Curl Request:

```bash
curl --request PATCH --header "Content-Type: application/json" --header "Authorization: Token f0a558e19062fb79ad67b20a561a2677396da026" --data '{"password":"manoj1999", "confirm_password": "manoj1999", "old_password": "amma1234"}' http://127.0.0.1:8000/accounts/password_update/46/
```

* 
    