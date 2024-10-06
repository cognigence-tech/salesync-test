from django.contrib import admin
from .models import Application, Connection


class ApplicationAdmin(admin.ModelAdmin):
  list_display = ('app_name', 'role', 'country', 'is_active', 'is_user_active')
  list_filter = ('role', 'country', 'is_active', 'is_user_active'
                 )  # Add filters


admin.site.register(Application, ApplicationAdmin)


class ConnectionAdmin(admin.ModelAdmin):
  # list_display = ('sender', 'receiver', 'user', 'is_active')
  list_filter = ('user', 'is_active', 'country')  # Add filters


admin.site.register(Connection, ConnectionAdmin)
