APT_OPTS="-uy -q --force-yes --allow-unauthenticated --no-install-recommends"

apt-get update $APT_OPTS

# install vim
apt-get install vim $APT_OPTS

echo mysql-server mysql-server/root_password password root | sudo debconf-set-selections

echo mysql-server mysql-server/root_password_again password root | sudo debconf-set-selections

apt-get install mysql-server $APT_OPTS

apt-get install build-essential python3-dev python3-setuptools $APT_OPTS

apt-get install python3-pip $APT_OPTS

pip3 install -r /vagrant/app/requirements.txt

exit 0
