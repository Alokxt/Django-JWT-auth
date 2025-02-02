from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role', 'is_staff'),
        }),
    )

    def has_module_permission(self, request):
        
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_school)




class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        return qs.filter(school=request.user.school_admin)  
    
    def has_module_permission(self, request):

   
        if not request.user.is_authenticated:  
            return False  
        return request.user.is_superuser or request.user.role == "school"
    

    def has_view_permission(self, request, obj=None):
       
        if request.user.is_superuser:
            return True
        return obj is None or obj.school == request.user.school_admin
    

    def has_add_permission(self, request):
        
        return request.user.is_superuser or request.user.role == "school"

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj and obj.school == request.user.school_admin

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


class acheivmentadmin(admin.ModelAdmin):
    list_display = ('name','description','achieved_on','linked_student_id','school')

    
    def get_form(self, request, obj=None, **kwargs):
    
        form = super().get_form(request, obj, **kwargs)
        
        if request.user.is_school:
            
            form.base_fields['student'].queryset = students.objects.filter(school = request.user.school_admin)
        
        return form
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        return qs.filter(st_school =request.user.school_admin)  
    
    def has_module_permission(self, request):

   
        if not request.user.is_authenticated:  
            return False  
        return request.user.is_superuser or request.user.role == "school"
    

    def has_view_permission(self, request, obj=None):
      
        if request.user.is_superuser:
            return True
        return obj is None or obj.school == request.user.school_admin
    

    def has_add_permission(self, request):
        
        return request.user.is_superuser or request.user.role == "school"

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj and obj.school == request.user.school_admin

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


class parentAdmin(admin.ModelAdmin):
    list_display = ('name', 'child_school','linked_student_id')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        return qs.filter(child_school=request.user.school_admin)  
    
    def has_module_permission(self, request):

   
        if not request.user.is_authenticated:  
            return False  
        return request.user.is_superuser or request.user.role == "school"
    

    def has_view_permission(self, request, obj=None):
        
        if request.user.is_superuser:
            return True
        return obj is None or obj.school == request.user.school_admin
    

    def has_add_permission(self, request):
       
        return request.user.is_superuser or request.user.role == "school"

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj and obj.school == request.user.school_admin

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)





admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Schools)
admin.site.register(students,StudentAdmin)
admin.site.register(Achievements,acheivmentadmin)
admin.site.register(parent,parentAdmin)