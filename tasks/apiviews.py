from tasks.models import Task, TaskHistory, STATUS_CHOICES
from tasks.serializers import TaskSerializer, TaskHistorySerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    ChoiceFilter,
    BooleanFilter,
    IsoDateTimeFilter,
)


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)
    completed = BooleanFilter()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serilaizer):
        serilaizer.save(user=self.request.user)


class TaskHistoryFilter(FilterSet):
    new_status = ChoiceFilter(choices=STATUS_CHOICES)
    updation_date = IsoDateTimeFilter()


class TaskHistoryViewSet(ReadOnlyModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter

    def get_queryset(self):
        return TaskHistory.objects.filter(
            task__id=self.kwargs["pk"],
            task__user=self.request.user
        )
