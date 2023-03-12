from django.urls import path, include

from django.contrib import admin

admin.autodiscover()
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/



urlpatterns = [
    # path('api-auth/', include('drf_social_oauth2.urls',namespace='drf')),
    # socials
    path("admin/", admin.site.urls),
    path("api/", include('api.urls')),
    path("", include('users.urls')),
    
]