from django.urls import path
from . import views

urlpatterns = [
    # Страницы кассира
    path('cashier-home/', views.cashier_home_page, name='cashier_home_page'),
    path('cashier-exit/', views.cashier_exit_page, name='cashier_exit_page'),
    path('cashier-exit/<int:id>/edit', views.cashier_edit_exit_task, name='cashier_edit_exit_task'),

    # Страницы менеджера
    path('manager-home/', views.manager_home_page, name='manager_home_page'),
    path('manager-entry/', views.manager_entry_page, name='manager_entry_page'),
    path('manager-entry/add-entry', views.manager_add_entry_task, name='manager_add_entry_task'),
    path('manager-entry/<int:id>/edit', views.manager_edit_entry_task, name='manager_edit_entry_task'),
    path('manager-entry/<int:id>/delete-entry', views.manager_delete_entry_task, name='manager_delete_entry_task'),
    path('manager-entry/add-counterparties', views.manager_add_counterparties, name='manager_add_counterparties'),
    path('manager-entry/manager_counterparties_list', views.manager_counterparties_list, name='manager_counterparties_list'),

    # Страницы охранника
    path('security-home/', views.security_home_page, name='security_home_page'),
    path('security-exit/', views.security_exit_page, name='security_exit_page'),
    path('security-entry/', views.security_entry_page, name='security_entry_page'),
    path('security-counterparties/', views.security_counterparties_page, name='security_counterparties_page'),
    path('security-counterparties/add-delivery', views.security_add_delivery, name='security_add_delivery'),
    path('security-tasks/', views.security_tasks_page, name='security_tasks_page'),
]