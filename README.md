# Welcome to PassionFroid API!

PassionFroid-Back is an API that communicates with an SQL database and Microsoft Azure services such as Images Cognitive Services and text recognition to provide data to the PassionFroid client.

## How to run locally
First step, you have to create a virtual environnment.

### Install venv
    pip install virtualenv
    
### Create venv and activate it
    python<version> -m venv <virtual-environment-name>
    source env/bin/activate

### Installing dependencies

    pip freeze > requirements.txt
    pip install -r requirements.txt
    
### Setup env file
You need to create an .env file and populate all of the following variables the project needs to work well with the database and Microsoft Azure.

FRONT_APP=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

API_HOST=

COGNITIVE_SERVICE_KEY=
AZURE_COGNITIVE_SERVICES_HOST=
AZURE_COGNITIVE_SERVICES_SUBSCRIPTION_KEY=
AZURE_COMPUTER_VISION_API_VERSION=

FRONT_APP_DEV=
DATABASE_NAME_DEV=
DATABASE_USER_DEV=
DATABASE_PASSWORD_DEV=
DATABASE_HOST_DEV=
DATABASE_PORT_DEV=

### Run the project
    python manage.py runserver

## How to deploy

To deploy app in Azure, create a static app then link your GitHub repository of your API.

Add environment variables to the settings configuration section