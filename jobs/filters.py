from django_filters import *

from .models import job_record
from django.db.models import Q

business_titles = job_record.objects.all().values_list('business_title').distinct()
civil_service_titles = job_record.objects.all().values_list('civil_service_title').distinct()
agencies =  job_record.objects.all().values_list('agency').distinct()

class JobFilter(FilterSet):
    def getbusinesstitle():
        # titles = job_record.objects.all().values_list('business_title').distinct()
        return  [(i,item[0]) for i,item in enumerate(business_titles)]
    def getcivilservicetitle():
                return  [(i,item[0]) for i,item in enumerate(civil_service_titles)]
    def getacgencies():
        return  [(i,item[0]) for i,item in enumerate(agencies)]

    wild_query = CharFilter(method='wild_search',label='Wild Search')
    civil_service_title= ChoiceFilter(choices=getcivilservicetitle(),method='custom_search',label='Civil Service Title',empty_label='Civil Service Title')

    # business_title = department = ModelChoiceFilter(
    #     queryset=job_record.objects.values('business_title').distinct(),method='business_search')
    business_title = ChoiceFilter(choices=getbusinesstitle(),method='custom_search',label='Business Title',empty_label='Business Title')
    agency = ChoiceFilter(choices=getacgencies(),method='custom_search',label='Agency',empty_label="Agency")

    def custom_search(self,queryset,name,query):
        if name=='business_title':
            print("BS",query,business_titles[int(query)][0])
            return queryset.filter(business_title=business_titles[int(query)][0])
        if name=='civil_service_title':
            print("CS",query,civil_service_titles[int(query)][0])
            return queryset.filter(civil_service_title=civil_service_titles[int(query)][0])
        if name=='agency':
            return queryset.filter(agency=agencies[int(query)][0])

    def wild_search(self, queryset,name,query):
        print("Wild" ,query)
        return queryset.filter(Q(agency__icontains=query)
        | Q(business_title__icontains=query)
        | Q(civil_service_title__icontains=query))
    class Meta:
        model = job_record
        fields = ['civil_service_title','business_title']
