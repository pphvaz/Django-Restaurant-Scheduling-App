from django.contrib import admin

from .models import User, Department, PreCreateUser, MonthlySchedule, DailySchedule

# Register your models here.
admin.site.register(User)
admin.site.register(Department)
admin.site.register(PreCreateUser)
admin.site.register(MonthlySchedule)
admin.site.register(DailySchedule)