# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.shortcuts import render, redirect  
from .models import User
from django.http import HttpResponse
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from celery import shared_task
import csv


class ListCsvUsersView(generics.ListAPIView):
    """ 
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(request, *args, **kwargs):
        queryset = User.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=export.csv'
        opts = queryset.model._meta
        field_names = ['candidateName,candidateGender']
        print(queryset)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for row in queryset:
          current_user = [row.name,row.gender]
          writer.writerow(current_user)
        return response


class ListUsersView(generics.ListAPIView):
    """ 
    Provides a get method handler.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        new_user = User.objects.create(
            name=request.data["name"],
            mobile_no=request.data["mobile_no"],
            gender=request.data["gender"]
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET candidate/:id/
    PUT candidate/:id/
    DELETE candidate/:id/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            current_user = self.queryset.get(pk=kwargs["pk"])
            return Response(UserSerializer(current_user).data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            current_user = self.queryset.get(pk=kwargs["pk"])
            serializer = UserSerializer()
            updated_user = serializer.update(current_user, request.data)
            return Response(UserSerializer(updated_user).data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            current_user = self.queryset.get(pk=kwargs["pk"])
            current_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
