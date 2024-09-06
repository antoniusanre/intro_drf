from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q


# Create your views here.

class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        institution_name = self.request.query_params.get('name', None)
        symbol = self.request.query_params.get('symbol',None)
        # if institution_name:
        #     queryset = queryset.filter(top_sellers__contains=[{'name': institution_name}])
        if institution_name:
            queryset = queryset.filter(Q(top_sellers__contains=[{'name': institution_name}]) | Q(top_buyers__contains=[{'name': institution_name}]))
        if symbol:
            queryset = queryset.filter(symbol__contains=symbol)
        return queryset
    
    def list(self, request):
        # cache_key = "institution trade"
        # cache_key = self.request.get_full_path()  # Define a unique cache key for this data
        cache_key = f"institution-trade:{self.request.query_params.get('name', None)}"  # Define a unique cache key for this data
        print(cache_key)
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        # print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response


class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get_queryset(self):
        queryset= super().get_queryset()
        sub_sector = self.request.query_params.get('sub_sector', None).split(',')
        if sub_sector:
            queryset = queryset.filter(sub_sector__in = [sub.strip() for sub in sub_sector])
        return queryset

    def list(self, request):
        sub_sector = self.request.query_params.get('sub_sector', None)
        cache_key = f"report:{sub_sector}"
        result = cache.get(cache_key)
        if not result:
            result = self.get_queryset()
            cache.set(cache_key, result, 60)
        result = self.serializer_class(result, many=True)
        print(result.data)

        return Response(result.data)
    
class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def get_queryset(self):
        queryset= super().get_queryset()
        sector = self.request.query_params.get('sector',None)
        if sector:
            queryset = queryset.filter(sector__exact = sector)
        return queryset

    def list(self, request):
        sub_sector = self.request.query_params.get('sector',None)
        cache_key = f"sector:{sub_sector}"
        result = cache.get(cache_key)
        if not result:
            result = self.get_queryset()
            cache.set(cache_key, result, 60)
        result = self.serializer_class(result, many=True)

        return Response(result.data)