from django.contrib import admin
from goals.models import Goal, GoalCategory, GoalComment, BoardParticipant, Board


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_deleted')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('is_deleted',)
    readonly_fields = ('created', 'updated',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'priority')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority')
    readonly_fields = ('created', 'updated',)


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text',)
    readonly_fields = ('created', 'updated',)


class BoardParticipantInline(admin.TabularInline):
    model = BoardParticipant
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        queryset = queryset.exclude(role=BoardParticipant.Role.owner)
        return queryset


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'participants_count', 'is_deleted')
    search_fields = ('title',)
    list_filter = ('is_deleted',)
    inlines = (BoardParticipantInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('participants')
        return queryset

    def owner(self, obj):
        return obj.participants.filter(role=BoardParticipant.Role.owner).get().user

    def participants_count(self, obj):
        """
        Владельца не считаем
        """
        return obj.participants.count() - 1

    owner.short_description = 'Владелец'
    participants_count.short_description = 'Количество участников'