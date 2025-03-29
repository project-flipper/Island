# Island
Server backend for [ClubPenguin](https://github.com/project-flipper/ClubPenguin).

# Setup
Install **Python 3.7+** and **virtualenv** if you haven't already. Clone the github repo into a local directory using this command (it is recommended to use SSH):
```bash
git clone git@github.com:project-flipper/Island.git 
```

Then move into the `island` directory (`cd ./island`) and setup a virtualenv (`python3 -m virtualenv env`).
After this is complete, activate your newly created environment:
```bash
# for windows
env\Scripts\activate

# for unix
source "./env/bin/activate"
```

Install [Poetry](https://python-poetry.org/) python dependency manager, [install instructions here](https://python-poetry.org/docs/#installation). Install required python dependencies:

```bash
poetry install
```

## Database
Install PostgreSQL server, create a file `.env` in same directory as `main.py` and add in the database details (ref: https://github.com/project-flipper/Island/blob/main/island/database/__init__.py)

Setup the database by running the following command

```bash
alembic upgrade head
```

Your environment is ready to run **Island** :)

# Usage
It is recommended to create and use a virtualenv. Then, to activate your virtualenv, and go to the source root directory and start the application by executing the following command:
```bash
uvicorn main:app
```
It will take seconds to load up and then everything will be up and running. Press CTRL-C to gracefully stop the server.
Enjoy!
