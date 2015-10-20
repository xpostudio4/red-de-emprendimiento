from django.contrib import admin
from .models import Organization, UserProfile, MailingList

class OrganizationAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

class MailingListAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MailingList, MailingListAdmin)
