APT_OPTS="-uy -q --force-yes --allow-unauthenticated --no-install-recommends"

apt-get update $APT_OPTS

# install vim
apt-get install vim $APT_OPTS

apt-get install sqlite3 libsqlite3-dev

apt-get install build-essential python3-dev python3-setuptools $APT_OPTS

apt-get install python3-pip $APT_OPTS

pip3 install -r /vagrant/app/requirements.txt

exit 0
