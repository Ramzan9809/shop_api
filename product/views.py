from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          CategoryListSerializer, CategoryDetailSerializer,
                          ReviewListSerializer, ReviewDetailSerializer) 


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
    categories = Category.objects.all()
    data = CategoryListSerializer(categories, many=True).data
    return Response(
        data=data, 
        status=status.HTTP_200_OK  
    )


@api_view(http_method_names=['GET'])
def category_detail_api_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            data={'detail': 'Not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    data = CategoryDetailSerializer(category).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )   


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