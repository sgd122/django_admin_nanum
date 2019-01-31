from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.response import Response
from django.http import JsonResponse

from service20.models import msch
from django.views import View

# api/moim 으로 get하면 이 listview로 연결

class Service20ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = msch
        fields = ('ms_id', 'ms_name')
        
class Service20ListView(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = Service20ListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)