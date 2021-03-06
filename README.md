# Bounty-O-Matic

## Installation

Ubuntu packages: `libxml2-dev`, `libxslt1-dev`, `libffi-dev`, `libcairo2`, `libpango1.0-0`, `libgeoip-dev`.

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

## Install fonts for bounty export (Linux)

```
mkdir -p /usr/share/fonts/truetype/google-fonts
find static/bountyomatic/fonts/ -name "Lato-*.ttf" -exec sudo install -m644 {} /usr/share/fonts/truetype/google-fonts/ \;
fc-cache -f
```

# Scheduled tasks

Just add:
- `./manage.py refresh_characters`
- `./manage.py refresh_battletags`
- `./manage.py refresh_realms`

to your crontabs.

For example:

```
* */20 * * * /var/www/bounty-o-matic.com/venv/bin/python /var/www/bounty-o-matic.com/manage.py refresh_realms
* */20 * * * /var/www/bounty-o-matic.com/venv/bin/python /var/www/bounty-o-matic.com/manage.py refresh_characters
* */20 * * * /var/www/bounty-o-matic.com/venv/bin/python /var/www/bounty-o-matic.com/manage.py refresh_battletags
```
