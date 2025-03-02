from rest_framework import serializers
from .models import Product, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source="category"
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), write_only=True, many=True, source="tags"
    )

    class Meta:
        model = Product
        fields = ["id", "name", "description",  "price", "category", "category_id", "tags", "tag_id", "stock_quantity", "image", "created_at", "user"]