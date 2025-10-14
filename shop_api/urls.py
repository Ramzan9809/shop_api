from django.contrib import admin
from django.urls import path
from product.views import ( ProductDetailAPIView, ProductListAPIView,
                            CategoryDetailAPIView, CategoryListAPIView,
                            ReviewDetailAPIView, ReviewListAPIView,
                            ProductReviewAPIView)
from users.views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView
from . import swagger
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import CustomTokenObtainPairView
from users.google_oauth import GoogleLoginAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/v1/products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('api/v1/categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('api/v1/reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('api/v1/reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),      
    path("api/v1/products/reviews/", ProductReviewAPIView.as_view(), name="products-reviews"),

    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('authorization/', AuthorizationAPIView.as_view(), name='authorization'),
    path('confirm-registration/', ConfirmUserAPIView.as_view(), name='confirm-registration'),

    path('confirm/', ConfirmUserAPIView.as_view()),

    path('jwt/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/users/google-login/', GoogleLoginAPIView.as_view()),
]

urlpatterns += swagger.urlpatterns