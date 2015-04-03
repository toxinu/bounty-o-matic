# Bounty-O-Matic

## Installation

Ubuntu packages: `libxml2-dev`, `libxslt1-dev`, `libffi-dev`, `libcairo2`i, `libpango1.0-0`, `libgeoip-dev`.

```
git clone git@github.com:socketubs/bounty-o-matic.git
cd HeadHunter
virtualenv venv -p /usr/bin/python3
source venv/source/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp bountyomatic/local_settings_example.py bountyomatic/local_settings.py
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
rm -r bountyomatic/*/migrations
./manage.py makemigrations accounts
./manage.py makemigrations bounties
./manage.py syncdb
./manage.py migrate
```
