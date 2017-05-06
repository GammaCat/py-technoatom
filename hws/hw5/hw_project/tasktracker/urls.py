from django.conf.urls import url

from .views import main
from .views import add_task
from .views import edit_task


urlpatterns = [

    url(r'^add-task$', add_task),
    url(r'^edit-task/(?P<ind>\d+)$', edit_task),
    url(r'^$', main),

]
