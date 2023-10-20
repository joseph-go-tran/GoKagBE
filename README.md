
![Logo](https://firebasestorage.googleapis.com/v0/b/gokag-19eac.appspot.com/o/GOKag.png?alt=media)


# GoKag - Datasets and Surveys

## Introduction
GoKag is an Ultimate Datasets and Surveys Management Platform.

At GoKag, we empower individuals, researchers, and organizations to harness the power of data and insights like never before. We understand the critical role that datasets and surveys play in shaping decisions, driving innovation, and fueling progress. That's why we've created a dedicated platform to simplify and streamline every aspect of dataset and survey management.



## Demo

You can perform live demo here. [Live Demo](https://data.gokag.id.vn/).


## File structure

```
.
├── api                   
│   ├── app.py         
│   ├── exceptions.py     
│   ├── mixins.py
│   ├── permissions.py
│   ├── routes.py 
│   ├── urls.py 
│   ├── utils.py 
│   └── firebase.py   
├── authentication
│   ├── models.py 
│   ├── serializer.py 
│   ├── views
│   |   ├── views_answer.py
│   |   └── views_datasets.py
│   └── tests.py   
├── datasets
│   ├── models.py 
│   ├── serializer.py 
│   ├── views.py
│   └── tests.py
├── GoKag
│   ├── urls.py
│   └── settings.py
├── questionnaire
│   ├── models.py 
│   ├── serializer.py 
│   ├── views
│   |   ├── views_question.py
│   |   └── views_questionnaire.py
│   └── tests.py 
├── upload
│   ├── views.py
│   └── tests.py
├── manage.py
├── requirements.txt     
└── ...
```
## Table of Contents

- [Tech Stack](#techstack)
- [Features](#features)
- [Environment Variables](#environment-variables)
- [Run Locally](#run-)
- [Development](#development)
- [Running tests](#running-tests)
- [Acknowledgements](#acknowledgements)
- [License](#license)
## Tech Stack

- Django
- Mailgun (Mail service)
- Sentry (Error handling)
- JWT (Authentication)
- PostgreSQL (Database)
- Firebase (Storage)
- Digital Ocean (Server)

## Features

1. Authentication
- Register by email
- Verify email
- Login
- JWT with Access Token and Refresh Token

2. Datasets
- Create datasets through excel files or from surveys
- Update dataset's information
- Like/Share dataset to social media
- Download dataset by xlsx
- Search/Filter/Tags
- Realtime notification when anyone likes your dataset

3. Visualize
- Display data as a table
- Visualize datasets into statistical charts

4. Surveys
- Create a set of questions to conduct surveys via forms (add, copy, delete, arrangement)
- Automatically create question sets through analyzing excel files
- Send survey for people to fill out
- Search/Filter/Pagination

5. User profile
- Update personal information
- Update avatar
- Manage your own datasets and surveys
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MAILGUN_DOMAIN`

`MAILGUN_API_KEY`

`SECRET_KEY_JWT`

`SENTRY_KEY`

`ONE_SIGNAL_APP_ID`

`ONE_SIGNAL_REST_API_KEY`


## Run Locally

Clone the project

```bash
  git clone https://github.com/lucqng111/GoKag.git
```

Go to the project directory

```bash
  cd GoKag
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Migration
```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

Start the server

```bash
  python3 manage.py runserver
```


## Development

To run program in product environment:

- docker and docker-compose
- git

1. Clone the reposity:

```bash
    git clone git clone https://github.com/lucqng111/GoKag.git
```

2. From within the repository directory, run:

```bash
    docker-compose up --build
```

## Acknowledgements

 - [Django](https://docs.djangoproject.com/en/4.1/)
 - [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
 - [Docker](https://www.docker.com/)


## Running Tests

To run tests, run the following command

```bash
  python3 manage.py test
```


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Support

For support, email joseph.tran.goldenowl@gmail.com or join our Slack channel.

