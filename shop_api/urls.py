from django.contrib import admin
from django.urls import path
from product.views import ( product_detail_api_view, product_list_api_view, 
                           category_detail_api_view, category_list_api_view,
                            review_detail_api_view, review_list_api_view, 
                            products_reviews_api_view)
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', product_list_api_view, name='product-list'),
    path('api/v1/products/<int:pk>/', product_detail_api_view, name='product-detail'),
    path('api/v1/categories/', category_list_api_view, name='category-list'),
    path('api/v1/categories/<int:pk>/', category_detail_api_view, name='category-detail'),
    path('api/v1/reviews/', review_list_api_view, name='review-list'),
    path('api/v1/reviews/<int:pk>/', review_detail_api_view, name='review-detail'),      
    path("api/v1/products/reviews/", products_reviews_api_view, name="products-reviews"),

    path('api/v1/users/register/', views.registration_api_view, name='register'),
    path('api/v1/users/login/', views.authorization_api_view, name='login'), 
    path('api/v1/users/confirm/', views.confirm_registration_api_view, name='login'), 
]
