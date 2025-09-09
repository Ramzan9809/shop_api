from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          CategoryListSerializer, CategoryDetailSerializer,
                          ReviewListSerializer, ReviewDetailSerializer,
                          ProductReviewSerializer) 


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializer(products, many=True).data
    return Response(
        data=data, 
        status=status.HTTP_200_OK  
    )


@api_view(http_method_names=['GET'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            data={'detail': 'Not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    data = ProductDetailSerializer(product).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    categories = Category.objects.annotate(products_count=Count('products'))
    
    serializer = CategoryListSerializer(categories, many=True)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(http_method_names=['GET'])
def category_detail_api_view(request, pk):
    try:
        category = Category.objects.annotate(products_count=Count('products')).get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            data={'detail': 'Not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewListSerializer(reviews, many=True).data
    return Response(
        data=data, 
        status=status.HTTP_200_OK  
    )       


@api_view(http_method_names=['GET'])
def review_detail_api_view(request, pk):        
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(
            data={'detail': 'Not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    data = ReviewDetailSerializer(review).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )



@api_view(http_method_names=['GET'])
def products_reviews_api_view(request):

    products = Product.objects.all()
    data = ProductReviewSerializer(products, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)