#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
echo "Django instance for: $APIS_RDF_ONTOLOGY ontology"
echo "Current dir: $(pwd)"
echo "Dir contents:\n$(ls -la)"
echo "Creating symlink to ontology..."
rm -f apis_ontology
ln -s apis-ontologies/$APIS_RDF_ONTOLOGY apis_ontology
echo "$(file apis_ontology)"
echo "Running Django management commands:"
echo "Migrating..."
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput
#ls /var/solr_new/paas_solr
#python manage.py build_solr_schema --configure-directory /var/solr_new/paas_solr/conf --reload-core default
#gunicorn apis.wsgi --timeout 120 --workers=3 --threads=3 --worker-connections=1000
gunicorn apis.wsgi -b 0.0.0.0:5000 --timeout 120 --workers=3 --threads=3 --worker-connections=1000
