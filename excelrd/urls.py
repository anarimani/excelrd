from django.contrib import admin
import django.urls
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Map root URL to login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', include('django.contrib.auth.urls')),  # includes login and logout URLs
    path('excelapp/', include('excelapp.urls', namespace='excelapp')),  # Include the app URLs under 'excelapp/' with namespace

]
