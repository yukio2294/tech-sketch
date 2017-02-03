# About

This is a sample application for TIS Technical Internship 2017 Winter.

This sample app created from Heroku Django Starter Template.
See also, [heroku-django-template](https://github.com/heroku/heroku-django-template)

# Getting Started

Execute the following commands to deploy to Heroku

    $ heroku create
    $ git push heroku master
    $ heroku config:set AMAZON_ML_ENDPOINT=<your_amazon_ml_endpoint_url>
    $ heroku config:set AMAZON_ML_MODEL_ID=<your_amazon_ml_model_id>
    $ heroku config:set API_GATEWAY_ENDPOINT=<your_api_gateway_endpoint_url>
    $ heroku run python manage.py migrate
