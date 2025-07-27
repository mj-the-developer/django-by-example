from django.db.models import Count
from rest_framework.generics import RetrieveAPIView, ListAPIView

from courses.api.pagination import StandardPagination
from courses.api.serializers import SubjectSerializer
from courses.models import Subject


class SubjectListView(ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class SubjectDetailView(RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
