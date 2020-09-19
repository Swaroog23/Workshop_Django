from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime
from datetime import date as d
from conference_rooms.models import Rooms, Reservation


class AddRoomView(View):

    """Class view made for adding room object to database and to show on main view."""

    def get(self, request):
        """Get function returns form on GET request."""
        return render(request, "add_room.html")

    def post(self, request):
        """Post function to validate and save object from given form on POST request.
        Checks if name is given and is not in database,
        if size is a postive int and sets projector status as True or False.
        Every error returns form with information about an error.
        Returns user to the main page when everything is alright."""

        name = request.POST.get("name")
        size = request.POST.get("size")
        proj = request.POST.get("projector")
        if proj == "on":
            proj = True
        else:
            proj = False
        if len(name) == 0:
            return render(
                request,
                "add_room.html",
                context={"err": "Error: Room must have a name."},
            )
        try:
            size = int(size)
            if size <= 0:
                return render(
                    request,
                    "add_room.html",
                    context={"err": "Error: Room size must be bigger than zero."},
                )
        except ValueError:
            return render(
                request, "add_room.html", {"err": "Error: Room size must be a number."}
            )
        try:
            Rooms.objects.get(name=name)
            return render(
                request,
                "add_room.html",
                context={"err": "Error: Room with this name already exists."},
            )
        except ObjectDoesNotExist:
            Rooms.objects.create(name=name, size=size, projector=proj)
            return HttpResponseRedirect("/room/")


class ModifyRoomView(View):
    """Class view for modifing room objects parameters"""

    def get(self, request, id):
        """Get function returns form and room object to modify on GET request"""
        room = Rooms.objects.get(id=id)
        return render(request, "modify_room.html", {"id": id, "room": room})

    def post(self, request, id):
        """Post function validates data given by form on POST request.
        Checks if name is taken by other object, checks if size is postivie int
        and sets True or False for projector.
        Every error returns form with information about an error and with old room values.
        If everything is ok, returns user to main page"""

        name = request.POST.get("name")
        size = request.POST.get("size")
        proj = request.POST.get("projector")
        room = Rooms.objects.get(pk=id)

        if name == "":
            return render(
                request,
                "modify_room.html",
                context={
                    "err": "Error: Room must have a name.",
                    "id": id,
                    "room": room,
                },
            )
        try:
            size = int(size)
            if size < 0:
                return render(
                    request,
                    "modify_room.html",
                    context={
                        "err": "Error: Room size must be a number bigger than zero.",
                        "id": id,
                        "room": room,
                    },
                )
        except ValueError:
            return render(
                request,
                "modify_room.html",
                context={
                    "err": "Error: Room size must be a number.",
                    "id": id,
                    "room": room,
                },
            )
        if proj == "on":
            proj = True
        else:
            proj = False
        room.name = name
        room.size = size
        room.projector = proj
        try:
            room.save()
        except IntegrityError:
            return render(
                request,
                "modify_room.html",
                context={
                    "err": "Error: Room with this name already exists.",
                    "id": id,
                    "room": room,
                },
            )
        return HttpResponseRedirect("/room/")


class RoomReservationView(View):
    """Class view for making a reservation on the room."""

    def get(self, request, id):
        """Get function returns form with todays date and room with give id on GET request"""
        room = Rooms.objects.get(pk=id)
        return render(
            request,
            "reservation.html",
            context={"id": id, "room": room, "date_now": d.today()},
        )

    def post(self, request, id):
        """Post function for validation data from given form.
        Checks if date is given, not from the past and not taken for this room.
        Every error returns form with information about an error.
        If everything is alright, returns user to the main page."""
        room = Rooms.objects.get(pk=id)
        date_reserved = request.POST.get("date")
        comment = request.POST.get("comm")
        if len(date_reserved) == 0:
            return render(
                request,
                "reservation.html",
                context={
                    "id": id,
                    "err": "Please select date",
                    "room": room,
                    "date_now": d.today(),
                },
            )
        try:
            Reservation.objects.get(date=date_reserved, room_id=room)
            return render(
                request,
                "reservation.html",
                context={
                    "id": id,
                    "err": "Date is taken, select other date",
                    "room": room,
                    "date_now": d.today(),
                },
            )
        except ObjectDoesNotExist:
            if datetime.strptime(date_reserved, "%Y-%m-%d").date() < d.today():
                return render(
                    request,
                    "reservation.html",
                    context={
                        "id": id,
                        "err": "Date cannot be from the past",
                        "room": room,
                        "date_now": d.today(),
                    },
                )
            else:
                Reservation.objects.create(
                    date=date_reserved, room_id=room, comment=comment
                )
        return HttpResponseRedirect("/room/")


def base(request):
    """View function for main page. Returns html with all the rooms
    and reservations made for today on each room.
    If there are no rooms, returns information for the user about it."""
    rooms = Rooms.objects.all().order_by("id")
    reservations = Reservation.objects.filter(date=d.today())
    reserv_list = []
    for reservation in reservations:
        reserv_list.append(reservation.room_id.id)
    if len(rooms) > 0:
        context = {"rooms": rooms, "reservations": reserv_list, "avaiable": d.today()}
    else:
        context = {"empty": "No rooms avaiable!"}

    return render(request, "base_temp.html", context)


def delete(request, id):
    """Delete function for button on main page.
    Deletes room and all reservations for that room."""
    room_to_del = Rooms.objects.get(pk=id)
    room_to_del.delete()
    return HttpResponseRedirect("/room/")


def show_room(request, id):
    """View function for shoing details for given room.
    Returns page with all the informations about the room and its reservations."""
    room = Rooms.objects.get(pk=id)
    return render(request, "room_view.html", {"room": room, "date_now": d.today()})
