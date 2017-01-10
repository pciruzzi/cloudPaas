# cloudPaas
Projet du Cloud Computing - 5ème anée INSA Toulouse - Ciruzzi, Gravouil, Kasry, Maldonado, Nguyen

## PyProxmox Installation
Having installed Python and `pip` (In Ubuntu: `sudo apt-get install python-pip`), just execute `sudo pip install pyproxmox requests`. The documentation of the API is [here](https://github.com/Daemonthread/pyproxmox).

## Usage
To execute the server: `python server.py <serverIP> <user> <password>`

## Create the virtual environment

virtualenv env 
source env/bin/activate 
pip3 install django 

TODO: Search the thing of requirements.txt and add it to the instructions 

# Create the MySQL database with the following credentials
Name -> cloud_pass

# Create also a user that will need to have all the permissions 
UserName -> insa
Password -> insa

# Install the database dependencies
sudo apt-get install libmysqlclient-dev
pip3 install mysqlclient

# Run the application
python3 manage.py runserver

# Save modifications made to a model
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser
admin
admin@test.com
adminadmin

python3-pip