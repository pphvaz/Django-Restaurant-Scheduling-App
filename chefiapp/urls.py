from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("profile/<int:id>/", views.profile_view, name="profile"),
    path("staff", views.staff_view, name="staff"),
    path("new_staff", views.new_staff, name="new_staff"),
    path("new_profile", views.new_staff, name="new_profile"),
    path("schedule/<int:user>", views.schedule_view, name="schedule"),
    path('get-schedule-data/', views.get_schedule_data, name='get_schedule_data'),
    path('update-schedule-data/', views.update_schedule_data, name='update_schedule_data'),
    path('save-schedule-data/', views.save_schedule_data, name='save_schedule_data'),
    path('new_month_data/<int:user>', views.new_month_data, name='new_month_data'),
    path('error-page/', views.error_page_view, name='error-page'),
    path("caixa", views.caixa_view, name="caixa"),

]