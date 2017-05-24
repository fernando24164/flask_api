APT_OPTS="-uy -q --force-yes --allow-unauthenticated --no-install-recommends"

apt-get update $APT_OPTS

apt-get install vim $APT_OPTS

apt-get install build-essential python3-dev python3-setuptools python3-pip $APT_OPTS

apt-get install ipython $APT_OPTS

pip3 install -r /vagrant/app/requirements.txt

exit 0
