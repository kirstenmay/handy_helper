from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^leave_job/(?P<job_id>\d+)', views.leave_job),
    url(r'^join_job/(?P<job_id>\d+)', views.join_job),
    url(r'^delete/(?P<job_id>\d+)', views.delete),
    url(r'^done/(?P<job_id>\d+)', views.done),
    url(r'^view_job/(?P<job_id>\d+)$', views.view_job),
    url(r'^edit_job/(?P<job_id>\d+)$', views.edit_job),
    url(r'change_job', views.change_job),
    url(r'^new_job$', views.new_job),
    url(r'^add_job$', views.add_job),
    url(r'^dashboard', views.dashboard),
    url(r'^log_out$', views.log_out),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^$', views.login_reg),
]