#!/bin/bash
#useradd -M celery
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
rm /app/apis_ontology
ln -s /app/apis-ontologies/$APIS_RDF_ONTOLOGY /app/apis_ontology
python manage.py collectstatic
python manage.py migrate
python manage.py collectstatic --noinput
#ls /var/solr_new/paas_solr
#python manage.py build_solr_schema --configure-directory /var/solr_new/paas_solr/conf --reload-core default
gunicorn apis.wsgi --timeout 120 --workers=3 --threads=3 --worker-connections=1000