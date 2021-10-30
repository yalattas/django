from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics, status

# Create your views here.
class MyFirstAPIView(generics.GenericAPIView):
    serializer_class = FirstApiSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Here is get description
        """
        try:
            employees = Employee.objects.all()
            serializer = self.serializer_class(employees, many=True)
            return Response(
                {
                    ('results'): (serializer.data),
                    ('status'):(200)
                },
                status=status.HTTP_200_OK)
        except:
            return Response(
                {
                    ('error'): ("no objects found"),
                    ('status'): (404)
                },
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Here is post
        """
        try:
            data = JSONParser().parse(request)
            serializer = AddNewEmployeeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    ('results'): (serializer.data),
                    ('status'):(201)
                },
                status=status.HTTP_201_CREATED)
        except:
            return Response(
                {
                    'error': ("bad request"),
                    ('status'): (400)
                },
                status=status.HTTP_400_BAD_REQUEST)