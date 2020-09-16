from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from datetime import datetime
from conference_rooms.models import Rooms, Reservation


class AddRoomView(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get("name")
        if len(name) == 0:
            return render(
                request, "add_room.html", {"err": "Error: Room must have a name."}
            )
        try:
            size = int(request.POST.get("size"))
            if size < 0:
                return render(
                    request,
                    "add_room.html",
                    {"err": "Error: Room size must be bigger than zero."},
                )
        except:
            return render(
                request, "add_room.html", {"err": "Error: Room size must be a number."}
            )
        proj = request.POST.get("projector")
        try:
            room = Rooms.objects.get(name=name)
            return render(
                request,
                "add_room.html",
                {"err": "Error: Room with this name already exists."},
            )
        except:
            if proj == "on":
                proj = True
            else:
                proj = False
            room = Rooms.objects.create(name=name, size=size, projector=proj)

            return HttpResponseRedirect("/room/")


class ModifyRoomView(View):
    def get(self, request, id):
        return render(request, "modify_room.html", {"id": id})
    
    def post(self, request, id):
        name = request.POST.get("name")
        size = request.POST.get("size")
        proj = request.POST.get("projector")
        try:
            room = Rooms.objects.get(pk=id)
        except:
            return render(
                request,
                "modify_room.html",
                {"err": "Error: Room with this id does not exists.",
                "id": id},
            )
        if len(name) == 0:
            return render(
                request,
                "modify_room.html",
                {"err": "Error: Room must have a name.",
                "id": id},
            )
        try:
            size = int(size)
        except:
            return render(
                request,
                "modify_room.html",
                {"err": "Error: Room size must be a number.",
                "id": id},
            )
        if proj == "on":
            proj = True
        else:
            proj = False
        try:
            Rooms.objects.get(name=name)
            return render(
                request,
                "modify_room.html",
                {"err": "Error: Room with this name already exists.",
                "id": id},
            )
        except:
            room.name = name
            room.size = size
            room.projector = proj
            room.save()
        return HttpResponseRedirect("/room/")


class RoomReservationView(View):
    def get(self, request, id):
        return render(request, "reservation.html", context={"id": id})

    def post(self, request, id):
        room = Rooms.objects.get(pk=id)
        date = request.POST.get("date")
        comment = request.POST.get("comm")
        try:
            Reservation.objects.get(date=date).filter(room_id=room)
            return render(request, "reservation.html", context={
                "id": id,
                "err": "Date is taken, select other date"
                })
        except:
            if datetime.strptime(date, "%Y-%m-%d") < datetime.now():
                return render(request, "reservation.html", context={
                    "id": id,
                    "err": "Date cannot be from the past"
                    })
            else:
                Reservation.objects.create(date=date, room_id=room, comment=comment)
        return HttpResponseRedirect("/room/")

def base(request): 
    rooms = Rooms.objects.all()
    if len(rooms) > 0:
        context = {"rooms": rooms}
    else:
        context = {"empty": "No rooms avaiable!"}
    return render(request, "base_temp.html", context)


def delete(request, id):
    room_to_del = Rooms.objects.get(pk=id)
    room_to_del.delete()
    return HttpResponseRedirect("/room/")


def show_room(request, id):
    room = Rooms.objects.get(pk=id)
    return render(request, "room_view.html", {"room": room})