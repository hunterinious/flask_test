# URL shortener


## Setup virtual environment

To create virtual environment you need to type the following command in the root directory:

`python3 -m venv env`

Then you need to install all the necessary requirements:

`pip install -r requirements.txt`


## Setup db 

First you need to create the database, go to root directory and type:

`docker-compose up db`

Then we need to run all migrations to create all required tables:

`flask db upgrade`

## Crontab

Finally we need to setup crontab job, which every hour sets `is_expired=True`for links that have expired:

`flask crontab add`


## Run app

In the root directory type the following command:

`flask run`


## Testing

For testing you need to setup test config, edit the following line in .env file in the root directory:

`ENV=test`

And then you can run tests:

`pytest`


## API

| URL | Method| description | params | required |
| --- | ----- |------------ | ------ | -------- |
| api/links/create |POST| creates a short link |`long_url` - original url| Yes |
|                  ||                      |`days` - how many days the link will be stored| No|                                        
| api/links/\<int:id\>/retrieve|GET|retrieves a short link by link id| | |
| api/links/\<int:id\>/redirect |GET|redirects to long url by link id| | |



