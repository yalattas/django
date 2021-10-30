from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
class MyFirstAPIView(APIView):
    serializer_class = FirstApiSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            employees = Employee.objects.all()
            serializer = self.serializer_class(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({('error'): ("Component not found.")}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = AddNewEmployeeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': ("bad request")}, status=status.HTTP_400_BAD_REQUEST)