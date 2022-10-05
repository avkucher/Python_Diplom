from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from django.db.models import Q
from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment
from goals.permissions import IsOwnerOrReadOnly
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(user_id=self.request.user.id, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.filter(user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(generics.CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]



class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    filterset_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'descriptions']

    def get_queryset(self):
        return Goal.objects.filter(user_id=self.request.user.id).filter(~Q(status=Goal.Status.archived))


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(user_id=self.request.user.id).filter(~Q(status=Goal.Status.archived))

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)






