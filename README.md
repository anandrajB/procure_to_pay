# SCF_BACKEND  

## TECHNOLOGY STACK
[![https://www.python.org/](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DJANGO](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org/)
[![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)

## INSTALLATION AND RUNNING **
```
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py migrate --run-syncdb
- python manage.py runserver
```
## TENANT PROCESS 
```
- python manage.py migrate_schemas  ( for schmeas migration )
- python manage.py create_tenant_superuser  ( superuser for tenant's )
```

## NEW DB CONFIG (POSTGRES) **
```
- python manage.py migrate 
- python manage.py makemigrations 
- python manage.py migrate --run-syncdb
```
## DUMP TEST DATA 

#### test credentials 
```
- python manage.py loaddata fixtures/accounts.json
- python manage.py loaddata fixtures/transactions.json
```
#### common
```
- python manage.py loaddata fixtures/data.json   
```
#### misc
```
- python manage.py loaddata fixtures/actions.json  
- python manage.py loaddata fixtures/currencies.json 
- python manage.py loaddata fixtures/countries.json 
```

\
***Important NOTE:*** *The data.json maintains all the currencies , countries , actions data*

## RUNNING TEST CASES **
```
- python manage.py test accounts
- python manage.py test transaction
```
## IMPORTANT LINKS

- [DB Diagram](https://dbdiagram.io/d/61b82d3b8c901501c0ef1a4f)

- [Postman collection](https://www.getpostman.com/collections/74a150a6a4ee22543b8c)

- [Documentation](https://documenter.getpostman.com/view/11858287/Uyr5pf1h)

- [Base url](https://venzoscf.herokuapp.com/)

- [Admin panel](https://venzoscf.herokuapp.com/admin/)

- [API-URL's](https://venzoscf.herokuapp.com/api-urls/)


## CREDENTIALS

#### ADMIN

| version  | Details |
| ------------- | ------------- |
| phone | 1471471471 |
| password  | admin123  |
| email | finflo@admin.com |


#### BUYER

| version  | Details |
| ------------- | ------------- |
| phone | 9677210269 |
| password  | admin123  |
| email | buyer@gmail.com |



## WORKING ENVIRONMENTS

- [TESTING](http://venzoscf.herokuapp.com)

- [PRODUCTION](http://167.71.238.26/)


## Environment Variables

- To run this project, you will need to add the following environment variables to your .env file
- Modify the following environment variables for your database setup

    - `ENGINE`
    - `NAME`
    - `USER`
    - `PASSWORD`
    - `HOST` 

- #### example 
```
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'name',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```


## SUPPORTED VERSIONS

| version  | End of support |
| ------------- | ------------- |
| django 3.2.5 LTS | April 2023 |
| python 3.8  | october 2024  |
|Django REST|-|

## Authors

- [@anandrajB](https://github.com/anandrajB)
- [@Mohamed-Sheik-Ali](https://github.com/Mohamed-Sheik-Ali)



## Appendix

#### ***NOTE 1*** : The ** indicated one are important and required commands

#### ***NOTE 2*** : Before running this project , check [PRODUCTION.md](https://github.com/venzo-tech/scfbackend/blob/master/PRODUCTION.md) file