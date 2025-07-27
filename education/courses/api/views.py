from django.db.models import Count
from rest_framework.generics import RetrieveAPIView, ListAPIView

from courses.api.serializers import SubjectSerializer
from courses.models import Subject


class SubjectListView(ListAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer


class SubjectDetailView(RetrieveAPIView):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
