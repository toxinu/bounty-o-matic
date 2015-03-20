# HeadHunter

## Installation

```
git clone git@github.com:socketubs/HeadHunter.git
cd HeadHunter
virtualenv venv -p /usr/bin/python3
source venv/source/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp headhunter/local_settings_example.py headhunter/local_settings.py
# Set Battlenet API keys in you local_settings
./manage.py syncdb
# Anwser yes to create super user (for admin)
./manage.py migrate
./manage.py runsslserver
```

And open `https://localhost:8000`. (**https !**)

## Reset database

```
rm db.sqlite3
rm headhunter/*/migrations/*.py
./manage.py syncdb
./manage.py makemigrations
./manage.py migrate
```
