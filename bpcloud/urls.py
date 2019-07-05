from django.urls import path
from . import views

urlpatterns = [
    path('home.html',           views.home),
    path('init_home/',          views.initHome),
    path('query_page/',         views.queryPageInfo),
    path('query_dustbin/',      views.queryDustbin),
    path('upload_file/',        views.uploadFile),
    # path('upload_dir/',         views.uploadDir),
    path('download/',           views.download),
    path('dfile_opera/',        views.dfileOpera),
    path('move_check/',         views.moveCheck),
    path('recovery_check/',     views.recoveryCheck),
    path('hash_check/',         views.hashCheck),
    # path('upload/',             views.upload),

]

