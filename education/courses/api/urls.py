from django.urls import include, path
from rest_framework import routers

from courses.api import views


app_name = 'courses'


router = routers.DefaultRouter()
router.register('subjects', views.SubjectViewSet)
router.register('courses', views.CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
