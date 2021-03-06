from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import (
    ERUOwner,
    ERU,
    Heop,
    Fact,
    FactPerson,
    Rdrt,
    RdrtPerson,
    PartnerSocietyDeployment,
)
from api.models import Country
from api.view_filters import ListFilter
from .serializers import (
    ERUOwnerSerializer,
    ERUSerializer,
    HeopSerializer,
    FactSerializer,
    RdrtSerializer,
    FactPersonSerializer,
    RdrtPersonSerializer,
    PartnerDeploymentSerializer,
)


class ERUOwnerViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ERUOwner.objects.all()
    serializer_class = ERUOwnerSerializer
    ordering_fields = ('created_at', 'updated_at',)

class ERUFilter(filters.FilterSet):
    deployed_to__isnull = filters.BooleanFilter(name='deployed_to', lookup_expr='isnull')
    deployed_to__in = ListFilter(name='deployed_to__id')
    class Meta:
        model = ERU
        fields = ('available',)

class ERUViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ERU.objects.all()
    serializer_class = ERUSerializer
    filter_class = ERUFilter

class HeopViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Heop.objects.all()
    serializer_class = HeopSerializer

class FactViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Fact.objects.all()
    serializer_class = FactSerializer

class RdrtViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Rdrt.objects.all()
    serializer_class = RdrtSerializer

class FactPersonViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = FactPerson.objects.all()
    serializer_class = FactPersonSerializer

class RdrtPersonViewset(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = RdrtPerson.objects.all()
    serializer_class = RdrtPersonSerializer

class PartnerDeploymentFilterset(filters.FilterSet):
    parent_society = filters.NumberFilter(name='parent_society', lookup_expr='exact')
    country_deployed_to = filters.NumberFilter(name='country_deployed_to', lookup_expr='exact')
    district_deployed_to = filters.NumberFilter(name='district_deployed_to', lookup_expr='exact')
    parent_society__in = ListFilter(name='parent_society__id')
    country_deployed_to__in = ListFilter(name='country_deployed_to__id')
    district_deployed_to__in = ListFilter(name='district_deployed_to__id')
    class Meta:
        model = PartnerSocietyDeployment
        fields = {
            'start_date': ('exact', 'gt', 'gte', 'lt', 'lte'),
            'end_date': ('exact', 'gt', 'gte', 'lt', 'lte'),
        }

class PartnerDeploymentViewset(viewsets.ReadOnlyModelViewSet):
    queryset = PartnerSocietyDeployment.objects.all()
    serializer_class = PartnerDeploymentSerializer
    filter_class = PartnerDeploymentFilterset
