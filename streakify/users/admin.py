from _operator import or_
from functools import reduce
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import admin as auth_admin
from django.db.models import Q
from streakify.users.forms import UserChangeForm, UserCreationForm
from streakify.users.models import User, UserProfile
from streakify.core.utils import optimized_queryset


User = get_user_model()

UserSearchFields = [
    "id",
    "user__username",
    "user__email",
]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["id", "username", "name", "is_superuser"]
    search_fields = ["name", "email", "username"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ["id", "user", "mobile"]
    search_fields = UserSearchFields
    get_queryset = optimized_queryset


    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(UserProfileAdmin, self).get_search_results(request, queryset, search_term)
        search_words = search_term.split(',')
        if search_words:
            q_objects = [Q(**{field + '__iexact': word})
                         for field in self.search_fields
                         for word in search_words]
            queryset |= self.model.objects.all().filter(reduce(or_, q_objects))

        return queryset, use_distinct