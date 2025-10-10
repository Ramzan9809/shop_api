from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, Category, Review
from common.validators import validate_user_age_from_token


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # Валидация конкретного поля
    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return value

    # Валидация всех данных сразу
    def validate(self, attrs):
        if attrs.get('title') and len(attrs['title']) < 3:
            raise ValidationError({"title": "Название должно содержать минимум 3 символа."})
        
        request = self.context.get('request')
        validate_user_age_from_token(request)
        return attrs


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return value


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError("Название категории слишком короткое.")
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError("Название категории слишком короткое.")
        return value


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if value < 1 or value > 10:
            raise ValidationError("Рейтинг (stars) должен быть от 1 до 10.")
        return value


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if value < 1 or value > 10:
            raise ValidationError("Рейтинг (stars) должен быть от 1 до 10.")
        return value


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "title", "reviews", "rating")

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([r.stars for r in reviews]) / reviews.count(), 2)
        return None
