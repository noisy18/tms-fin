from django.urls import path
from tms_admin import views
from counterparties.views import create_counterparty_pass, edit_counterparty

urlpatterns = [
    # Основные страницы
    path('home/', views.admin_home_page, name='admin_home_page'),
    path('entry/', views.entry_page, name='entry_page'),
    path('exit/', views.exit_page, name='exit_page'),
    path('counterparties/', views.counterparties_page, name='counterparties_page'),
    path('counterparties-list/', views.counterparties_list, name='counterparties_list'),
    path('tasks/', views.tasks_page, name='tasks_page'),
    path('panel/', views.admin_panel, name='admin_panel'),
    path('archive/', views.tasks_archive, name='tasks_archive'),

    # Дополнительные страницы
    path('tasks/add-text', views.add_text_task, name='add_text_task'),
    path('tasks/add-entry', views.add_entry_task, name='add_entry_task'),
    path('tasks/add-exit', views.add_exit_task, name='add_exit_task'),
    path('counterparties/add-counterparties', views.add_counterparties, name='add_counterparties'),
    path('counterparties/add-delivery', views.add_delivery, name='add_delivery'),

    path('tasks/<int:id>/edit-text', views.edit_text_task, name='edit_text_task'),
    path('tasks/<int:id>/edit-entry', views.edit_entry_task, name='edit_entry_task'),
    path('tasks/<int:id>/edit-exit', views.edit_exit_task, name='edit_exit_task'),

    path('tasks/completed', views.completed_tasks, name='completed_tasks'),
    path('counterparties/counterparties_archive', views.counterparties_archive, name='counterparties_archive'),

    path('panel/<int:id>/edit-user', views.edit_user_form, name='edit_user_form'),
    path('panel/<int:id>/delete_user/', views.delete_user, name='delete_user'),

    # Представления
    path('tasks/<int:id>/delete-text', views.delete_text_task, name='delete_text_task'),
    path('tasks/<int:id>/delete-entry', views.delete_entry_task, name='delete_entry_task'),
    path('tasks/<int:id>/delete-exit', views.delete_exit_task, name='delete_exit_task'),

    path('tasks/<int:id>/complete-text', views.mark_text_task_complete, name='mark_text_task_complete'),
    path('tasks/<int:id>/complete-entry', views.mark_entry_task_complete, name='mark_entry_task_complete'),
    path('tasks/<int:id>/complete-exit', views.mark_exit_task_complete, name='mark_exit_task_complete'),
    path('tasks/<int:id>/complete-counterparty', views.mark_counterparties_complete, name='mark_counterparties_complete'),
    path('tasks/<int:id>/complete-delivery', views.mark_delivery_complete, name='mark_delivery_complete'),

    # views.py из apps.counterparties
    path('counterparties-list/<int:counterparty_id>/create', create_counterparty_pass, name='create_counterparty_pass'),
    path('counterparties-list/<int:counterparty_id>/edit', edit_counterparty, name='edit_counterparty'),
]