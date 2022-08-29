#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
echo "Django instance for project: $APIS_RDF_ONTOLOGY"
echo "Current dir: $(pwd)"
ls -la
pwd
rm -f apis_ontology
ln -s apis-ontologies/$APIS_RDF_ONTOLOGY apis_ontology
ls -la
pwd
echo $APIS_RDF_ONTOLOGY
python manage.py migrate
python manage.py collectstatic --noinput
#ls /var/solr_new/paas_solr
#python manage.py build_solr_schema --configure-directory /var/solr_new/paas_solr/conf --reload-core default
gunicorn apis.wsgi --timeout 120 --workers=3 --threads=3 --worker-connections=1000