from django.urls import path
from .views import home, add_patient, view_patterns, view_exported_result
from django.contrib.auth import views as auth_views  
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),  # Homepage
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # This should now point to the correct view
    path('add/', views.add_patient, name='add_patient'),
    path('patterns/', views.view_patterns, name='view_patterns'),
    path('exported-result/', view_exported_result, name='view_exported_result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


