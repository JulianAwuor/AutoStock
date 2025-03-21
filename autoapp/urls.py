
from django.contrib import admin
from django.urls import path
from autoapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('newstock', views.newstock, name='newstock'),
    path('newsupplier/', views.newsupplier, name='newsupplier'),
    path('charts/', views.charts, name='charts'),
    path('forgot/', views.forgot, name='forgot'),
    path('stocks/', views.stocks, name='stocks'),
    path('existingsupplier/', views.existingsupplier, name='existingsupplier'),
    path('utilitiesanimation/', views.utilitiesanimation, name='utilitiesanimation'),
    path('utilitiesborder/', views.utilitiesborder, name='utilitiesborder'),
    path('utilitiescolor/', views.utilitiescolor, name='utilitiescolor'),
    path('utilitiesother/', views.utilitiesother, name='utilitiesother'),
    path('delete/<int:id>', views.delete),
    path('deletesupplier/<int:id>', views.deletesupplier),
    path('editstock/<int:id>', views.editstock, name='editstock'),
    path('update/<int:id>', views.update, name='update'),
    path('editsupplier/<int:id>', views.editsupplier, name='editsupplier'),
    path('updatesupplier/<int:id>', views.updatesupplier, name='updatesupplier'),
    path('totalstock/', views.totalstock, name='totalstock'),
    path("addsale", views.addsale, name="addsale"),
    path('salesummary/', views.salesummary, name='salesummary'),
    path('saleslist/', views.saleslist, name='saleslist'),





]
