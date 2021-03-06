"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from config import settings
from file import views as fileviews
from member import views as memberviews
from paging import views as pagingviews
from solve import views as solveviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', memberviews.main),
    path('login/', memberviews.login),
    path('member/', include('member.urls')),
    path('solve/', include('solve.urls')),
    path('file/', include('file.urls')),
    path('problem_list/', solveviews.problem_list),
    path('problem_upload/', solveviews.problem_upload),
    path('today_exam/', solveviews.today_exam),
]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
