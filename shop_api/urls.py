from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', views.product_list_api_view, name='product-list'),
    path('api/v1/products/<int:pk>/', views.product_detail_api_view, name='product-detail'),
    path('api/v1/categories/', views.category_list_api_view, name='category-list'),
    path('api/v1/categories/<int:pk>/', views.category_detail_api_view, name='category-detail'),
    path('api/v1/reviews/', views.review_list_api_view, name='review-list'),
    path('api/v1/reviews/<int:pk>/', views.review_detail_api_view, name='review-detail'),      
    path("api/v1/products/reviews/", views.products_reviews_api_view, name="products-reviews"),

]
