
######################
# Urls description
######################

Description of the urls

/project/create

- create a new project

/project/create/[PROJECT_ID]

- list all project configurations for PROJECT_ID
- change project configurations for PROJECT_ID

/project/[PROJECT_ID]/stage

- create a stage configuration for PROJECT_ID

##############
# Database
##############

To generate initial data and create de tables on the database run the following command:

python manage.py syncdb
