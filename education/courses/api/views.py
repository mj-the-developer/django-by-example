from rest_framework.generics import RetrieveAPIView, ListAPIView

from courses.api.serializers import SubjectSerializer
from courses.models import Subject


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
