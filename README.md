# Island
Server backend for [ClubPenguin](https://github.com/clubpenguin-html5/ClubPenguin).

# Setup
Install **Python 3.7+** and **virtualenv** if you haven't already. Clone the github repo to your local directory, using the command for example (It is recommended to use SSH)
```bash
git clone git@github.com:clubpenguin-html5/Island.git 
```

Then move into `island` directory (`cd ./island`), then setup virtualenv for python 3 (`python3 -m virtualenv env`). After you setup virtualenv, activate virtualenv
```bash
# for windows
"env/scipts/activate"

# for unix
source "./env/bin/activate"
```
After that make sure to install all required python dependencies,
```bash
pip install -r requirements.txt
pip install uvicorn
```
Your environment is all setup to run **Island** :)

# Usage
It is recommended to create and use a virtualenv, if so activate your virtualenv, and go to the source root directory.

You can then start the application by executing the following command
```bash
uvicorn main:app
```
