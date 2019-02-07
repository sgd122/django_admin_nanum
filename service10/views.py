from django.shortcuts import render
from rest_framework import generics, serializers
from django.http import HttpResponse,Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from service10.models import *

# Create your views here.

class Service10AuthListSerializer(serializers.ModelSerializer):

    class Meta:
        model = vm_nanum_stdt
        fields = ('apl_id', 'apl_nm','apl_nm_e','univ_cd','univ_nm')



class Service10AuthListView(generics.ListAPIView):
    queryset = vm_nanum_stdt.objects.all()
    serializer_class = Service10AuthListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


def post_login(request):
	ida = request.POST.get('user_id', None)
	passa = request.POST.get('user_pw', None)
	#created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)

	created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()


	if not created_flag:
		message = "Fail"
	else:
		message = "Ok"
	context = {'message': message}

	#return HttpResponse(json.dumps(context), content_type="application/json")
	return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



def authView(request):
    context = None
    return render(request, 'service10/Service10Auth.html', context)
