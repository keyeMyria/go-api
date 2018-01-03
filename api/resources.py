from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from .models import (
    DisasterType,
    KeyFigure,
    Snippet,
    Event,
    EventContact,
    Country,
    Region,
    Appeal,
    FieldReport,
    FieldReportContact,
    Profile,
    ActionsTaken,
    Action,
    ERUOwner,
    ERU,
    Heop,
)
from .authentication import ExpiringApiKeyAuthentication
from .authorization import FieldReportAuthorization, UserProfileAuthorization
from .public_resource import PublicModelResource


# Duplicate resources that do not query 's related objects.
# https://stackoverflow.com/questions/11570443/django-tastypie-throws-a-maximum-recursion-depth-exceeded-when-full-true-on-re
class RelatedAppealResource(ModelResource):
    class Meta:
        queryset = Appeal.objects.all()
        filtering = {
            'status': ('exact', 'iexact', 'in'),
            'atype': ('exact', 'in'),
            'country': ('exact', 'in'),
        }


class RelatedEventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        filtering = {
            'eid': ('exact', 'in'),
        }
        authorization = Authorization()


class RelatedFieldReportResource(ModelResource):
    class Meta:
        queryset = FieldReport.objects.all()


class RelatedUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        authentication = ExpiringApiKeyAuthentication()
        authorization = Authorization()


class DisasterTypeResource(ModelResource):
    class Meta:
        queryset = DisasterType.objects.all()
        resource_name = 'disaster_type'
        allowed_methods = ['get']
        authorization = Authorization()


class RegionResource(ModelResource):
    class Meta:
        queryset = Region.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()


class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()


class ActionResource(ModelResource):
    class Meta:
        queryset = Action.objects.all()
        authorization = Authorization()
        allowed_methods = ['get']


class ActionsTakenResource(ModelResource):
    actions = fields.ToManyField(ActionResource, 'actions', full=True, null=True)
    class Meta:
        queryset = ActionsTaken.objects.all()
        resource_name = 'actions_taken'
        allowed_methods = ['get']
        authorization = Authorization()


class KeyFigureResource(ModelResource):
    class Meta:
        queryset = KeyFigure.objects.all()
        resource_name = 'key_figure'


class SnippetResource(ModelResource):
    class Meta:
        queryset = Snippet.objects.all()


class EventContactResource(ModelResource):
    class Meta:
        queryset = EventContact.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        authentication = ExpiringApiKeyAuthentication()


class EventResource(PublicModelResource):
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', full=True)
    appeals = fields.ToManyField(RelatedAppealResource, 'appeals', null=True, full=True)
    field_reports = fields.ToManyField(RelatedFieldReportResource, 'field_reports', null=True, full=True)
    countries = fields.ToManyField(CountryResource, 'countries', full=True)
    regions = fields.ToManyField(RegionResource, 'regions', null=True, full=True, use_in='detail')
    contacts = fields.ToManyField(EventContactResource, 'eventcontact_set', full=True, null=True, use_in='detail')
    key_figures = fields.ToManyField(KeyFigureResource, 'keyfigure_set', full=True, null=True, use_in='detail')
    snippets = fields.ToManyField(SnippetResource, 'snippet_set', full=True, null=True, use_in='detail')

    # Don't return field reports if the user isn't authenticated
    def dehydrate_field_reports(self, bundle):
        if self.has_valid_api_key(bundle.request):
            return bundle.data['field_reports']
        else:
            return None

    # Attach data from model instance methods
    def dehydrate(self, bundle):
        bundle.data['start_date'] = bundle.obj.start_date()
        bundle.data['end_date'] = bundle.obj.end_date()
        return bundle

    class Meta:
        queryset = Event.objects.select_related().all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'name': ('exact', 'iexact'),
            'appeals': ALL_WITH_RELATIONS,
            'eid': ('exact', 'in'),
            'countries': ('exact', 'in'),
            'regions': ('exact', 'in'),
            'created_at': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'disaster_start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
        }
        ordering = [
            'disaster_start_date',
            'created_at',
            'name',
            'dtype',
            'summary',
            'num_affected',
            'auto_generated',
        ]


class AppealResource(ModelResource):
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', full=True, null=True)
    country = fields.ForeignKey(CountryResource, 'country', full=True, null=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True, null=True, use_in='detail')
    class Meta:
        queryset = Appeal.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'event': ALL_WITH_RELATIONS,
            'aid': ('exact', 'in'),
            'status': ('exact', 'iexact', 'in'),
            'code': ('exact', 'in'),
            'amount_requested': ('gt', 'gte', 'lt', 'lte', 'range'),
            'amount_funded': ('gt', 'gte', 'lt', 'lte', 'range'),
            'num_beneficiaries': ('gt', 'gte', 'lt', 'lte', 'range'),
            'atype': ('exact', 'in'),
            'country': ('exact', 'in'),
            'region': ('exact', 'in'),
            'created_at': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'end_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
        }
        ordering = [
            'start_date',
            'end_date',

            'name',
            'aid',
            'atype',
            'dtype',

            'num_beneficiaries',
            'amount_requested',
            'amount_funded',

            'event',
            'country',
            'region',
            'status',
            'code',
            'sector',
        ]


class UserResource(ModelResource):
    profile = fields.ToOneField('api.resources.ProfileResource', 'profile', full=True)
    subscription = fields.ToManyField('notifications.resources.SubscriptionResource', 'subscription', full=True)
    class Meta:
        queryset = User.objects.all()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'patch']
        filtering = {
            'username': ('exact', 'startswith'),
        }
        authentication = ExpiringApiKeyAuthentication()
        authorization = UserProfileAuthorization()


class ProfileResource(ModelResource):
    class Meta:
        queryset = Profile.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        authorization = UserProfileAuthorization()


class FieldReportContactResource(ModelResource):
    class Meta:
        queryset = FieldReportContact.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        authentication = ExpiringApiKeyAuthentication()


class FieldReportResource(ModelResource):
    user = fields.ForeignKey(RelatedUserResource, 'user', full=True, null=True)
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', full=True)
    countries = fields.ToManyField(CountryResource, 'countries', full=True)
    regions = fields.ToManyField(RegionResource, 'regions', null=True, full=True, use_in='detail')
    event = fields.ForeignKey(RelatedEventResource, 'event', full=True, null=True)
    contacts = fields.ToManyField(FieldReportContactResource, 'fieldreportcontact_set', full=True, null=True, use_in='detail')
    actions_taken = fields.ToManyField(ActionsTakenResource, 'actionstaken_set', full=True, null=True)
    class Meta:
        queryset = FieldReport.objects.all()
        resource_name = 'field_report'
        always_return_data = True
        authentication = ExpiringApiKeyAuthentication()
        authorization = FieldReportAuthorization()
        filtering = {
            'event': ALL_WITH_RELATIONS,
            'created_at': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'summary': ('exact', 'in'),
            'id': ('exact', 'in'),
            'rid': ('exact', 'in'),
            'countries': ('exact', 'in'),
            'regions': ('exact', 'in'),
            'status': ('exact', 'in'),
            'request_assistance': ('exact')
        }
        ordering = [
            'created_at',
            'summary',
            'event',
            'dtype',
            'status',
            'request_assistance',

            'num_injured',
            'num_dead',
            'num_missing',
            'num_affected',
            'num_displaced',
            'num_assisted',
            'num_localstaff',
            'num_volunteers',
            'num_xpats_delegates',

            'gov_num_injured',
            'gov_num_dead',
            'gov_num_missing',
            'gov_num_affected',
            'gov_num_displaced',
            'gov_num_assisted',
        ]



class ERUOwnerResource(ModelResource):
    eru_set = fields.ToManyField('api.resources.ERUResource', 'eru_set', null=True, full=True)
    class Meta:
        queryset = ERUOwner.objects.all()
        authentication = ExpiringApiKeyAuthentication()
        resource_name = 'eru_owner'
        allowed_methods = ['get']
        filtering = {
            'country': ('exact', 'in'),
        }


class RelatedERUOwnerResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    class Meta:
        queryset = ERUOwner.objects.all()
        allowed_methods = ['get']


class ERUResource(ModelResource):
    countries = fields.ToManyField(CountryResource, 'countries', full=True, null=True)
    eru_owner = fields.ForeignKey(RelatedERUOwnerResource, 'eru_owner', full=True)
    class Meta:
        queryset = ERU.objects.all()
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'eru_owner': ALL_WITH_RELATIONS,
            'type': ('exact', 'in'),
            'countries': ('in'),
        }
        allowed_methods = ['get']


class HeopResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    event = fields.ForeignKey(EventResource, 'event', null=True)
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', null=True, full=True)
    class Meta:
        queryset = Heop.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'country': ('exact', 'in'),
            'region': ('exact', 'in'),
            'linked_event': ('exact', 'in'),
            'person': ('exact', 'in'),
        }
        ordering = ['end_date', 'start_date']
