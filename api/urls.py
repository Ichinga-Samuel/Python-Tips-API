from django.urls import path
from .views import TipViewSet, TipsCreateView, TipsEditView, TagViewSet, TipsSearchView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tips', TipViewSet, basename='tips')

router.register('tags', TagViewSet, basename='tags')

app_name = 'api'

urlpatterns = [
    path('api/search/', TipsSearchView.as_view(), name='search'),
    path('api/create_tip/', TipsCreateView.as_view(), name='create-tips'),
    path('api/edit/<int:pk>/', TipsEditView.as_view(), name='edit-tips')
]

urlpatterns += router.urls
