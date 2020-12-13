## Podcast application

Flask application where users can listen to podcasts and find their friends recommendations.

Go to https://shareyourbestpodcast.com/



### Set up before running the application

create `gunicorn_setup.py` and add the configuration:

```
raw_env = [
    "SECRET_KEY=<SECRET_KEY>",
    "DATABASE_URL=<DATABASE_URL>",
    "ELASTICSEARCH_URL=<ELASTICSEARCH_URL>",
    "USERS_PER_PAGE=5",
    "PHOTO_PATH=<APP_PATH>/app/static/images/photos"
    ]
```
### Run the app

Run then application with :

```
gunicorn -c gunicorn_setup.py -b localhost:<APPLICATION_PORT> -w 4 podcast_social_network:app &
```

