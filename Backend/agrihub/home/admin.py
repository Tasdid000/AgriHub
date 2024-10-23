from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name", "phone_Number", "is_admin", "is_expert"]
    list_filter = ["is_admin", "is_expert"]
    
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "phone_Number", "image", "address"]}),
        ("Permissions", {"fields": ["is_admin", "is_expert", "is_active", "email_verified"]}),
        ("Farm Information", {"fields": ["Farm_Name", "Farm_Type", "Farm_Size", "Farm_Location"]}),
    ]
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "image", "address", "name", "phone_Number", "password1", "password2", "is_expert", "Farm_Name", "Farm_Type", "Farm_Size", "Farm_Location"],
            },
        ),
    ]
    
    search_fields = ["email", "name", "phone_Number"]
    ordering = ["email", "name", "phone_Number"]
    filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

class Contactadmin(admin.ModelAdmin):
    list_display = ["id", "First_Name", "Last_Name","Email"]
    class Meta:
        model = Contact
admin.site.register(Contact, Contactadmin)

class Farm_Typeadmin(admin.ModelAdmin):
    list_display = ["Farm_Type"]
    class Meta:
        model = Farm_Type
admin.site.register(Farm_Type, Farm_Typeadmin)

class Blogadmin(admin.ModelAdmin):
    list_display = ["id","Blog_title", "date" , "category"]
    class Meta:
        model = Blog
admin.site.register(Blog, Blogadmin)

class Appointment_time_slotadmin(admin.ModelAdmin):
    list_display = ["time"]
    class Meta:
        model = Appointment_time_slot
admin.site.register(Appointment_time_slot, Appointment_time_slotadmin)

class Video_conference_appointmentadmin(admin.ModelAdmin):
    list_display = ["UserId","Topic","Date", "Time"]
    class Meta:
        model = Video_conference_appointment
admin.site.register(Video_conference_appointment, Video_conference_appointmentadmin)

class Government_Supportadmin(admin.ModelAdmin):
    list_display = ["SupportId","Title","date", "category"]
    class Meta:
        model = Government_Support
admin.site.register(Government_Support, Government_Supportadmin)

