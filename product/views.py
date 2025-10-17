from django.db.models import Count
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    CategoryListSerializer, CategoryDetailSerializer,
    ReviewListSerializer, ReviewDetailSerializer,
    ProductReviewSerializer
)
from common.permissions import IsOwner, IsAnonymous, CanEditWithIn15minutes, IsMaderator  
from rest_framework.permissions import SAFE_METHODS
from common.validators import validate_user_age_from_token
from django.core.cache import cache


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsOwner()]
        return [IsAnonymous() | IsMaderator()]  
    
    def perform_create(self, serializer):
        validate_user_age_from_token(self.request)
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        cached_data = cache.get("product_list")
        if cached_data:
            print("Redis")
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().get(self, request, *args, **kwargs)
        print("Postgres")
        if response.data.get("total", 0) > 0:
            cache.set("product_list", response.data, timeout=300)
        return response


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAnonymous() | IsMaderator()]
        return [IsOwner() & CanEditWithIn15minutes() | IsMaderator()]


class CategoryListAPIView(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.annotate(products_count=Count('products'))


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.annotate(products_count=Count('products'))


class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer


class ProductReviewAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductReviewSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
