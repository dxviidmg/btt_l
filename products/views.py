from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.response import Response


class BrandViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    
    def create(self, request):
        data = request.data
        brand_id = request.data.pop('brand')
        brand = Brand.objects.get(id=brand_id)
        instance = Product.objects.create(**data, brand=brand)
        serializer = ProductSerializer(instance, context = {'request':request}, many = False)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = request.user
        instance = self.get_object()
        if user.is_anonymous:
            #Log visit product
            visits = Visit.objects.create(product=instance)

        serializer = ProductSerializer(instance, context = {'request':request}, many = False)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()

        serializer = self.serializer_class(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()

            #Product update email notification
            msg = 'The product with sku ' + instance.sku + ' was updated.' + '\nThe attributes are:\n'
            attributes = list('*' + k for k in request.data.keys())
            attributes = '\n'.join(list(attributes))
            msg = msg + attributes

            admin_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
            try:
                send_mail('Product update', msg, None, admin_emails, fail_silently=False)
            except Exception as e:
                print('Error sending emails', e)
        
        return Response(serializer.data)