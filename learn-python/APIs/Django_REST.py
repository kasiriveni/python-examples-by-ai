# Django REST Framework: REST API Example

# Install Django and DRF
print("pip install django djangorestframework")

# Add 'rest_framework' to INSTALLED_APPS in settings.py

# Define a serializer in serializers.py
print("from rest_framework import serializers\nclass ItemSerializer(serializers.Serializer):\n    id = serializers.IntegerField()\n    name = serializers.CharField(max_length=100)")

# Define a view in views.py
print("from rest_framework.views import APIView\nfrom rest_framework.response import Response\nclass ItemView(APIView):\n    def get(self, request, item_id):\n        return Response({\"item_id\": item_id})")

# Add a URL pattern in urls.py
print("from django.urls import path\nfrom .views import ItemView\nurlpatterns = [path('items/<int:item_id>/', ItemView.as_view())]")
