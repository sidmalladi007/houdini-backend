from django.conf.urls import url
from houdini import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^consumers/$', views.ConsumerList.as_view()),
    url(r'^consumers/(?P<pk>[0-9]+)/$', views.ConsumerDetail.as_view()),
    url(r'^pros/$', views.ProList.as_view()),
    url(r'^pros/(?P<pk>[0-9]+)/$', views.ProDetail.as_view()),
    url(r'^favorites/$', views.FavoriteList.as_view()),
    url(r'^favorites/(?P<pk>[0-9]+)/$', views.FavoriteDetail.as_view()),
    url(r'^projects/$', views.ProjectList.as_view()),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view()),
    url(r'^conversations/$', views.ConversationList.as_view()),
    url(r'^conversations/(?P<pk>[0-9]+)/$', views.ConversationDetail.as_view()),
    url(r'^messages/$', views.MessageList.as_view()),
    url(r'^messages/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view()),
    url(r'^schedulings/$', views.SchedulingList.as_view()),
    url(r'^schedulings/(?P<pk>[0-9]+)/$', views.SchedulingDetail.as_view()),
    url(r'^confirmed-appointments/$', views.ConfirmedAppointmentList.as_view()),
    url(r'^confirmed-appointments/(?P<pk>[0-9]+)/$', views.ConfirmedAppointmentDetail.as_view()),
    url(r'^quotes/$', views.QuoteList.as_view()),
    url(r'^quotes/(?P<pk>[0-9]+)/$', views.QuoteDetail.as_view()),
    url(r'^confirmed-prices/$', views.ConfirmedPriceList.as_view()),
    url(r'^confirmed-prices/(?P<pk>[0-9]+)/$', views.ConfirmedPriceDetail.as_view()),
    url(r'^twilio-sms/$', views.twilio_sms),
    url(r'^twilio-verify/$', views.twilio_verify),
    url(r'^issue-key/$', views.issue_key)
]

# urlspatterns = format_suffix_patterns(urlpatterns)
