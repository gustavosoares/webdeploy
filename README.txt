
######################
# Urls description
######################

Description of the urls

GET /project - list projects
POST /project - save a project
GET /project/PROJECT_ID - list project_id
GET /project/create - create a new project

GET /project/PROJECT_ID/stage - list and configure stage for project_id
POST /project/PROJECT_ID/stage - saves stage configuration for project_id

GET /project/PROJECT_ID/manage - manage project_id (execute tasks and so on)

GET /project/PROJECT_ID/fabfile - configure fabfile for project_id
POST /project/PROJECT_ID/fabfile - saves fabfile configuration for project_id
GET /project/PROJECT_ID/fabfile/view - view fancy fabfile with syntax highlight for project_id


##############
# Database
##############

To generate initial data and create de tables on the database run the following command:

python manage.py syncdb
