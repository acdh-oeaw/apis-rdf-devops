# from apis_core.apis_entities.models import *
# from apis_core.apis_relations.models import *
# from apis_core.apis_vocabularies.models import *
from django.core.management.base import BaseCommand, CommandError
import importlib
# import random


class Command(BaseCommand):

    def handle(self, *args, **options):

        script = importlib.import_module(f"apis_ontology.ontology_specific_scripts.{options['ontology_script']}")
        script.run()

    def add_arguments(self, parser):

        parser.add_argument("ontology_script")