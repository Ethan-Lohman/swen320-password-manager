# password-manager

This project is a password manager for the class of Introduction to Software Testing. It functions as a basic password manager, with a focus on the ability to test the software, there is also a selenium test file which is in a seperate document.

## Getting started

1. `make setup`
- If the make setup does not work do the following:
  1. source .env
  2. make migrate
2. `make run`

### Folder structure

- **crypto** (this is the password generator part, along with the encryption/decryption)
- **web** (this is the web program itself.)
    - **accounts** (Holds the database for the accounts and allows the interaction of them)
    - **core** (Holds the rest of the program other than the accounts)
    - **templates** (Holds the HTML)
        - **accounts**
        - **core**
    - **__init__**
- **.env**
- **config.py**
- **manage.py**
- **makefile**
- **README.md**

## Testing

1. Make statement
2. Make branch
3. Make test

## Credit
Tutorial used to get started: [link](https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/)

Team - Ethan Lohman, Rainey Biggerstaff, Brady Wire
