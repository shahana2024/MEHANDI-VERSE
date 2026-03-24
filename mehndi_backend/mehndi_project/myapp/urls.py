from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from myapp import views

from mehndi_project import settings

urlpatterns = [
    
    path('index/',views.index),
    path('forgot_password_get/',views.forgot_password_get),
    path('forgot_password/',views.forgot_password),
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('admin_home/',views.admin_home),
    path('admin_view_design/<id>',views.admin_view_design),
    path('admin_view_user/',views.admin_view_user),
    path('admin_reject_artist/<id>',views.admin_reject_artist),
    path('admin_accept_artist/<id>',views.admin_accept_artist),
    path('admin_view_artist/',views.admin_view_artist),
    path('admin_view_complaints/',views.admin_view_complaints),
    path('admin_send_reply/',views.admin_send_reply),
    path('admin_view_feedback/',views.admin_view_feedback),
    path('admin_accept_product/<id>',views.admin_accept_product),
    path('admin_reject_product/<id>',views.admin_reject_product),
    path('admin_view_product/<id>',views.admin_view_product),
    path('admin_add_recommend_get/',views.admin_add_recommend_get),
    path('admin_add_recommend_post/',views.admin_add_recommend_post),
    path('admin_edit_design_get/<id>',views.admin_edit_design_get),
    path('admin_edit_recommend_post/',views.admin_edit_design_post),
    path('admin_delete_design/<id>',views.admin_delete_design),
    
    
    
    
    path('artist_register/',views.artist_register),
    path('userlogin',views.userlogin),
    path('user_register/',views.user_register),
    path('upload_design/',views.upload_design),
    path('view_designs/',views.view_designs),
    path('delete_design/',views.delete_design),
    path('update_design/',views.edit_design),
    path('add_product/',views.add_product),
    path('view_products/',views.view_product),
    path('delete_product/',views.delete_product),
    path('update_product/',views.edit_product),
    path('arti_view_profile/',views.artiview_profile),
    path('artiupdate_profile/',views.update_profile),
    path('update_profile/',views.update_profile),
    path('user_change_password/',views.fchange_password_post),
    path('view_artist_requests/',views.view_artist_requests),
    path('arti_view_chat/<int:id1>/<int:id2>/', views.arti_view_chat),
    path('arti_send_chat', views.arti_send_chat),
    path('arti_send_chat_image/',views.arti_send_chat_image),
    path('view_product_orders/',views.view_product_orders),
    path('update_order_status/',views.update_order_status),
    path('update_request_amount/',views.update_request_amount),
    path('update_request_status/',views.update_request_status),


    path('view_all_artists/',views.view_all_artists),
    path('view_gallery/',views.view_gallery),
    path('userview_chat/<int:id1>/<int:id2>/',views.userview_chat),
    path('usersend_chat',views.usersend_chat),
    path('usersend_chat_image/',views.usersend_chat_image),
    path('send_booking_request/',views.send_booking_request),
    path('user_view_products/',views.user_view_products),
    path('place_order/',views.place_order),
    path('view_bookings/',views.view_bookings),
    path('view_artist_bookings/',views.view_artist_bookings),
    path('update_booking_status/',views.update_booking_status),
    path('payment_success/',views.payment_success),
    path('submit_feedback/',views.submit_feedback),
    path('user_update_profile/',views.userupdate_profile),
    path('recommend-mehndi/', views.recommend_mehndi),
    path('view_complaints/', views.view_complaints),
    path('send_complaint/', views.send_complaint),
    path('reply_complaint/', views.reply_complaint),
    path('view_profile/', views.view_profile),

]