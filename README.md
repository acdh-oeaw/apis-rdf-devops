# APIS RDF DEVOPS (working but still experimental)

## how to set up locally

### pre-requisites

* Have a local mysql server installed, ideally version 5.7, since this is what production uses (a persistence image might be integrated here in the future)

* Create a database and a user for your project, e.g. 

```
CREATE DATABASE apis_rdf_test_db;
CREATE USER 'apis_rdf_test_user'@'localhost' IDENTIFIED BY 'apis_rdf_test_password';
GRANT ALL PRIVILEGES ON apis_rdf_test_db.* TO 'apis_rdf_test_user'@'localhost';
FLUSH PRIVILEGES;
```

### setup

clone repo and recursively all its submodules, go into it:

```
git clone --recurse-submodules git@gitlab.com:acdh-oeaw/apis/apis-rdf-devops.git
cd apis-rdf-devops/
```

the ontology to be used must be symlinked into the repo root, for example like this:
```
rm apis_ontology # delete hard-wired placeholder
ln -s apis-ontologies/jelinek/ apis_ontology
```

Append at the end of file `apis_ontology/settings/server_settings.py` your db credentials (WARNING: Take care to not commit them), 
for example:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apis_rdf_test_db',
        'USER': 'apis_rdf_test_user',
        'PASSWORD': 'apis_rdf_test_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

From here onwards, there are two ways to set up the python environment:
* with a docker dev container in VS Code
* with a python virtual environment via `pipenv`  (and arbitrary IDE utilizing this environment)

### dev container in VS Code

TODO Matthias: fill in instruction

### pipenv

At the repo's root, set up your environment, and activate it:
```
pipenv install
pipenv shell
```


### django setup

Either within your dev container or virtual python environment, run the `manage.py` at the project's root with the corresponding settings from the ontology module, like so:
```
python manage.py version --settings=apis_ontology.settings.server_settings
```

If a fresh DB was set up, then it needs to be migrated:
```
python manage.py migrate --settings=apis_ontology.settings.server_settings
```

Start a django shell:
```
python manage.py shell --settings=apis_ontology.settings.server_settings
```
Create test admin user within shell:
```
from django.contrib.auth.models import User
User.objects.create_superuser('test_admin', None, 'test_password')
```

Within django shell, create the properties defined in the ontology (work-around for now as properties are instances instead of classes, due to a complicated trade-off):
```
from apis_ontology.models import construct_properties
construct_properties()
```
You can verify the properties:
```
from apis_core.apis_relations.models import Property
Property.objects.all() # shoud return a queryset
```

Run server:
```
python manage.py runserver --settings=apis_ontology.settings.server_settings
```

## ontology specific scripts

Projects occasionally need some processing logic only within the project scope. In order to avoid cluttering the main code base, project specific scripts can be run, by placing them in a subfolder `ontology_specific_scripts` in the respective ontology folder. For example the jelinek project has a script under path `apis_ontology/ontology_specific_scripts/import_tei.py`, this can be run like so:
```
python manage.py run_ontology_script import_tei --settings=apis_ontology.settings.server_settings
```
