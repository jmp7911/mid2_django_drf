from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# BaseUserAdmin 임포트


# BaseUserAdmin 기능을 커스텀 역시 가능
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email')
    list_display_links = ('email', )
    list_filter = ('email', )
    search_fields = ('email', )

    fieldsets = (
        ("info", {'fields': ('email', 'password' ,'created_at', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', )}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", 'profile_image'),
            },
        ),
    )
    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('email', 'created_at', )
        else:
            return ('created_at', )


admin.site.register(models.User, UserAdmin)
