from rest_framework.serializers import Serializer

from coems.models import Category, Product


class CategorySerializer(Serializer):
    class Meta:
        model = Category
        fields = ('name', 'description', 'icon')

class ProductSerializer(Serializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'tovar', 'category', 'price')