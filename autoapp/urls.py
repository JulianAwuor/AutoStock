
from django.contrib import admin
from django.urls import path
from autoapp import views
from .views import weekly_sales_data
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
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
    path('api/weekly-sales-data/', views.weekly_sales_data, name='weekly_sales_data'),
    path('api/low-stock-alerts/', views.low_stock_alert, name='low_stock_alert'),
    path('product_tracker/<int:product_id>/', views.product_tracker, name='product_tracker'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('download_report_pdf/', views.download_report_pdf, name='download_report_pdf'),
    path('register_employee/', views.register_employee, name='register_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('edit_employee/<int:user_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:user_id>/', views.delete_employee, name='delete_employee'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('receipt/<int:transaction_id>/', views.receipt, name='receipt'),
    path('download_receipt/<int:transaction_id>/', views.download_receipt, name='download_receipt'),




]
