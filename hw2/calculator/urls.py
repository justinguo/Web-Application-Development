from django.conf.urls import url, patterns, include
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'calculator.views.requestHandler'),
    url(r'^input$', 'calculator.views.input'),
)
