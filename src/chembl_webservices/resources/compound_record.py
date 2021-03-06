__author__ = 'mnowotka'

from chembl_webservices.core.utils import NUMBER_FILTERS, CHAR_FILTERS, FLAG_FILTERS
from tastypie import fields
from tastypie.resources import ALL
from chembl_webservices.core.resource import ChemblModelResource
from chembl_webservices.core.meta import ChemblResourceMeta
from chembl_webservices.core.serialization import ChEMBLApiSerializer
from django.db.models import Prefetch

from chembl_core_model.models import CompoundRecords
from chembl_core_model.models import Docs
from chembl_core_model.models import MoleculeDictionary

from chembl_webservices.core.fields import monkeypatch_tastypie_field
monkeypatch_tastypie_field()

# ----------------------------------------------------------------------------------------------------------------------


class CompoundRecordsResource(ChemblModelResource):

    molecule_chembl_id = fields.CharField('molecule__chembl_id')
    document_chembl_id = fields.CharField('doc__chembl_id')
    src_id = fields.IntegerField('src_id')

    class Meta(ChemblResourceMeta):
        queryset = CompoundRecords.objects.all().filter(removed=False)
        excludes = ['filename', 'updated_by', 'updated_on', 'removed', 'src_compound_id', 'src_compound_id_version',
                    'load_date', 'curated', 'ridx', 'cidx', 'job_id', 'log_id', 'molregno_fixed', 'molregno_comment',
                    'molregno_sv']
        resource_name = 'compound_record'
        collection_name = 'compound_records'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})
        prefetch_related = [
                            Prefetch('doc', queryset=Docs.objects.only('chembl')),
                            Prefetch('molecule', queryset=MoleculeDictionary.objects.only('chembl')),
                            ]
        filtering = {
            'compound_key': CHAR_FILTERS,
            'compound_name': CHAR_FILTERS,
            'molecule_chembl_id': ALL,
            'document_chembl_id': ALL,
            'curated': FLAG_FILTERS,
            'src_id': NUMBER_FILTERS,
        }
        ordering = [field for field in list(filtering.keys()) if not ('comment' in field or 'description' in field)]

# ----------------------------------------------------------------------------------------------------------------------
