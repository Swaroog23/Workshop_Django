"""Workshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from conference_rooms.views import AddRoomView, base, delete, ModifyRoomView, RoomReservationView, show_room

urlpatterns = [
    path("admin/", admin.site.urls),
    path("room/", base),
    path("room/new/", AddRoomView.as_view()),
    path("room/delete/<int:id>", delete),
    path("room/modify/<int:id>", ModifyRoomView.as_view()),
    path("room/reserve/<int:id>", RoomReservationView.as_view()),
    path("room/<int:id>", show_room)
]
