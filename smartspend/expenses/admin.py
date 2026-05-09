from django.contrib import admin
from django.contrib.auth.models import User
from .models import Expense, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    actions = ['approve_users', 'decline_users']

    def approve_users(self, request, queryset):
        for profile in queryset:
            profile.status = 'approved'
            profile.save()
            profile.user.is_active = True
            profile.user.save()
    approve_users.short_description = 'Approve selected users'

    def decline_users(self, request, queryset):
        for profile in queryset:
            profile.status = 'declined'
            profile.save()
            profile.user.is_active = False
            profile.user.save()
    decline_users.short_description = 'Decline selected users'

admin.site.register(Expense)
admin.site.register(UserProfile, UserProfileAdmin)