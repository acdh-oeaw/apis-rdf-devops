from django.core.management.base import BaseCommand, CommandError
from apis_core.apis_entities.models import *
from apis_core.apis_relations.models import *
from apis_core.apis_vocabularies.models import *
from apis_ontology.models import *
from apis_core.helper_functions import caching


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        
        parser.add_argument("model_class_to_process")
    
    def handle(self, *args, **options):
        field_tmp_mapping = {
            "review": 'review = models.BooleanField(default=False, help_text="Should be set to True, if the data record holds up quality standards.")',
            "start_date": 'start_date = models.DateField(blank=True, null=True) # WARNING: Unless you provide a custom parsing logic, the exposed date field would only allow YYYY-MM-DD format. Perhaps put a CharField instead, and reparse later?',
            "start_start_date": 'start_start_date = models.DateField(blank=True, null=True) # WARNING: Unless you provide a custom parsing logic, the exposed date field would only allow YYYY-MM-DD format. Perhaps put a CharField instead, and reparse later?',
            "start_end_date": 'start_end_date = models.DateField(blank=True, null=True) # WARNING: Unless you provide a custom parsing logic, the exposed date field would only allow YYYY-MM-DD format. Perhaps put a CharField instead, and reparse later?',
            "end_date": 'end_date = models.DateField(blank=True, null=True) # WARNING: Unless you provide a custom parsing logic, the exposed date field would only allow YYYY-MM-DD format. Perhaps put a CharField instead, and reparse later?',
            "end_start_date": 'end_start_date = models.DateField(blank=True, null=True) # WARNING: Unless you provide a custom parsing logic, the exposed date field would only allow YYYY-MM-DD format. Perhaps put a CharField instead, and reparse later?',
            "end_end_date": 'end_end_date = models.DateField(blank=True, null=True) # WARNING: Unless you provide a custom parsing logic, the exposed date field would only allow YYYY-MM-DD format. Perhaps put a CharField instead, and reparse later?',
            "start_date_written": 'start_date_written = models.CharField(max_length=255, blank=True, null=True, verbose_name="Start")',
            "end_date_written": 'end_date_written = models.CharField(max_length=255, blank=True, null=True, verbose_name="End")',
            "text": 'text = models.ManyToManyField("apis_metainfo.Text", blank=True)',
            "collection": 'collection = models.ManyToManyField("apis_metainfo.Collection")',
            "status": 'status = models.CharField(max_length=100)',
            "source": 'source = models.ForeignKey("apis_metainfo.Source", blank=True, null=True, on_delete=models.SET_NULL)',
            "references": 'references = models.TextField(blank=True, null=True)',
            "notes": 'notes = models.TextField(blank=True, null=True)',
            "published": 'published = models.BooleanField(default=False)',
        }
    
        def update_field_counter_if_true(te, field_dict, field_name):
            if getattr(te, field_name) is True:
                field_dict[field_name] = field_dict.get(field_name, 0) + 1
    
        def update_field_counter_if_not_none(te, field_dict, field_name):
            val = getattr(te, field_name)
            if val is not None and val != "":
                field_dict[field_name] = field_dict.get(field_name, 0) + 1
    
        def update_field_counter_if_some_related(te, field_dict, field_name):
            if len(getattr(te, field_name).all()) != 0:
                field_dict[field_name] = field_dict.get(field_name, 0) + 1
        
        def check_tempentityclass():
            tec_fields_counter_dict = {}
            for tec in TempEntityClass.objects.all():
                entity_class_context = ("EntityClass: ", tec.self_contenttype.model_class())
                fields_counter_dict = tec_fields_counter_dict.get(entity_class_context, {})
                update_field_counter_if_true(tec, fields_counter_dict, "review")
                update_field_counter_if_not_none(tec, fields_counter_dict, "start_date")
                update_field_counter_if_not_none(tec, fields_counter_dict, "start_start_date")
                update_field_counter_if_not_none(tec, fields_counter_dict, "start_end_date")
                update_field_counter_if_not_none(tec, fields_counter_dict, "end_date")
                update_field_counter_if_not_none(tec, fields_counter_dict, "end_start_date")
                update_field_counter_if_not_none(tec, fields_counter_dict, "end_end_date")
                update_field_counter_if_not_none(tec, fields_counter_dict, "start_date_written")
                update_field_counter_if_not_none(tec, fields_counter_dict, "end_date_written")
                update_field_counter_if_some_related(tec, fields_counter_dict, "text")
                update_field_counter_if_some_related(tec, fields_counter_dict, "collection")
                update_field_counter_if_not_none(tec, fields_counter_dict, "status")
                update_field_counter_if_not_none(tec, fields_counter_dict, "source")
                update_field_counter_if_not_none(tec, fields_counter_dict, "references")
                update_field_counter_if_not_none(tec, fields_counter_dict, "notes")
                update_field_counter_if_true(tec, fields_counter_dict, "published")
                if fields_counter_dict != {}:
                    tec_fields_counter_dict[entity_class_context] = fields_counter_dict
                
            return tec_fields_counter_dict
        
        def check_temptriple():
            tt_fields_counter_dict = {}
            for tt in TempTriple.objects.all():
                entity_class_subj = tt.subj.__class__
                entity_class_obj = tt.obj.__class__
                property_class = tt.prop
                temptriple_context = ("TempTriple (subj, obj, prop): ", entity_class_subj, entity_class_obj, property_class)
                fields_counter_dict = tt_fields_counter_dict.get(temptriple_context, {})
                update_field_counter_if_true(tt, fields_counter_dict, "review")
                update_field_counter_if_not_none(tt, fields_counter_dict, "start_date")
                update_field_counter_if_not_none(tt, fields_counter_dict, "start_start_date")
                update_field_counter_if_not_none(tt, fields_counter_dict, "start_end_date")
                update_field_counter_if_not_none(tt, fields_counter_dict, "end_date")
                update_field_counter_if_not_none(tt, fields_counter_dict, "end_start_date")
                update_field_counter_if_not_none(tt, fields_counter_dict, "end_end_date")
                update_field_counter_if_not_none(tt, fields_counter_dict, "start_date_written")
                update_field_counter_if_not_none(tt, fields_counter_dict, "end_date_written")
                update_field_counter_if_not_none(tt, fields_counter_dict, "status")
                update_field_counter_if_not_none(tt, fields_counter_dict, "references")
                update_field_counter_if_not_none(tt, fields_counter_dict, "notes")
                if fields_counter_dict != {}:
                    tt_fields_counter_dict[temptriple_context] = fields_counter_dict
                
            return tt_fields_counter_dict

        def print_tmp_fields_tec(model_fields_counter_dict, prefix_str):
            for model_class, fields_counter_dict in model_fields_counter_dict.items():
                print(f"\n#New fields to be manually added to {model_class}:")
                for field, count in fields_counter_dict.items():
                    print(f"{prefix_str}{field_tmp_mapping[field]}", f"# number of occurrences: {count}")

        def print_tmp_fields_tt(model_fields_counter_dict, prefix_str):
            for model_class, fields_counter_dict in model_fields_counter_dict.items():
                new_fields_on_reification = ""
                for field, count in fields_counter_dict.items():
                    new_fields_on_reification += f"\n{prefix_str}{field_tmp_mapping[field]}"\
                        f"# number of occurrences: {count}"
                print(
                    f"\nNew Reification class needed:"
                    f"\nbetween class (as 'subject'): {model_class[1].__name__}"
                    f"\nand class (as 'object'): {model_class[2].__name__}"
                    f"\nreplacing current property: {model_class[3]}"
                    f"\n\nCurrently there are TempTriple with these subjects, objects, property"
                    f" with these fields and number of occurrences:"
                    + new_fields_on_reification
                    + f"\n\nThe new Reification pattern should look like this:"
                    f"\n{model_class[1].__name__} -'prop_entity_to_reification'-> 'NewReificationClass'"
                    f" -'prop_reification_to_entity'-> {model_class[2].__name__}"
                    f"\n\nwhere you need to create:"
                    f"\n'prop_entity_to_reification'"
                    f"\n'prop_reification_to_entity'"
                    f"\n'NewReificationClass'"
                    f"\nTake the fields from above and add them to 'NewReificationClass'\n\n"
                )
        
        def copy_fields_from_tempentityclass(tec_fields_counter_dict, prefix_str):
            for entity_class, fields_counter_dict in tec_fields_counter_dict.items():
                for entity_instance in entity_class[1].objects.all():
                    for field_old in fields_counter_dict.keys():
                        field_new = f"{prefix_str}{field_old}"
                        if "ManyToManyField" in field_tmp_mapping[field_old]:
                            m2m_manager_old = getattr(entity_instance, field_old)
                            m2m_manager_new = getattr(entity_instance, field_new)
                            for related_instance in m2m_manager_old.all():
                                m2m_manager_new.add(related_instance)
                        else:
                            setattr(entity_instance, field_new, getattr(entity_instance, field_old))
                    entity_instance.save()
        
        def copy_fields_from_temptriple(tt_fields_counter_dict):
            for temptriple_context, fields_counter_dict in tt_fields_counter_dict.items():
                entity_class_subj = temptriple_context[1]
                entity_class_obj = temptriple_context[2]
                prop_instance = temptriple_context[3]
                for temptriple in TempTriple.objects.filter(
                    subj__self_contenttype=caching.get_contenttype_of_class(entity_class_subj),
                    obj__self_contenttype=caching.get_contenttype_of_class(entity_class_obj),
                    prop=prop_instance,
                ):
                    #TODO: Replace these if here
                    
                    # check for old employment relations
                    if (
                        entity_class_subj is Person
                        and entity_class_obj is Institution
                        and prop_instance == Property.objects.get(name="was employed at")
                    ):
                        # create an employment reification, fetch data from temptriple
                        employment = Employment.objects.create(
                            salary=int(temptriple.notes), # careful about something like this
                            employment_begin=temptriple.start_date_written,
                            employment_end=temptriple.end_date_written,
                        )
                        employment.save()
                        # relate subject entity of temptriple to reification
                        Triple.objects.create(
                            subj=temptriple.subj,
                            obj=employment,
                            prop=Property.objects.get(name="had (employment)"),
                        )
                        # relate object entity of temptriple to reification
                        Triple.objects.create(
                            subj=employment,
                            obj=temptriple.obj,
                            prop=Property.objects.get(name="(employment) at"),
                        )
                        # finally delete temptriple
                        temptriple.delete()
                    # same for supervisor relation
                    elif (
                        entity_class_subj is Person
                        and entity_class_obj is Person
                        and prop_instance == Property.objects.get(name="is supervisor of")
                    ):
                        supervision = Supervision.objects.create(
                            task_area=temptriple.notes,
                            supervision_begin=temptriple.start_date_written,
                            supervision_end=temptriple.end_date_written,
                        )
                        supervision.save()
                        Triple.objects.create(
                            subj=temptriple.subj,
                            obj=supervision,
                            prop=Property.objects.get(name="carries (supervision)"),
                        )
                        Triple.objects.create(
                            subj=supervision,
                            obj=temptriple.obj,
                            prop=Property.objects.get(name="under (supervision)"),
                        )
                        temptriple.delete()
                    # add more cases
                    # elif ():
                    #   ...
                
                # finally, delete the property
                prop_instance.delete()
                
            # finally, iterate over all remaining temptriples, carry them over to new ones, delete
            for tt in TempTriple.objects.all():
                Triple.objects.create(subj=tt.subj, obj=tt.obj, prop=tt.prop)
                tt.delete()

        model_class = options["model_class_to_process"]
        if model_class == "tec":
            tec_fields_prefix = "tmp_"
            tec_fields_counter_dict = check_tempentityclass()
            print_tmp_fields_tec(tec_fields_counter_dict, prefix_str=tec_fields_prefix)
            # copy_fields_from_tempentityclass(tec_fields_counter_dict, prefix_str=tec_prefix)
        elif model_class == "tt":
            tt_fields_counter_dict = check_temptriple()
            print_tmp_fields_tt(tt_fields_counter_dict, prefix_str="")
            # copy_fields_from_temptriple(tt_fields_counter_dict)
        else:
            raise Exception("no valid model_class was passed. Use either 'tec' or 'tt'")
        