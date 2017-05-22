# Flask_api

Just another example to make a API REST with Flask

## Beginning

To up the virtual machine go to the project folder and type

```Shell
$ vagrant up
```

If you don't have Vagrant you can make a virtual environment with python 3 and execute in local.

```Shell
$ pip install virtualenv
```

Go to a folder where you hold your virtual environments

```Shell
$ virtualenv virtualenvFlask -p /usr/bin/python3
```

Activate virtual environment

```Shell
$ source virtualenvFlask/bin/activate
```

Go to project folder and install the requirements

```Shell
$ pip install -r requirements.txt
```

You also need to create the database, if you want to change the name of the database
you need to change **config.py** the SQLALCHEMY_DATABASE_URI

```Python
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                        'weather.sqlite')
```

and create the database in our basedir

```Shell
$ touch weather.sqlite
```

Make the migrations to create the models in the database

```Shell
python3 manage.py migrate
```
