# Conference_rooms_workshop
Coders Lab workshop exercise and my first Django app. 
Task is to create web app with ability to make reservations, edit, and add conference rooms.

Viwes:

In views.py are views used in this project. There are 3 classes and 3 functions.

Classes:

AddRoomView: View for adding new room to the database. On GET it returns form, on POST it validates and add object to the database, while redirectiong user to main page if everything is alright. Checks if name is taken, size is postive integer and sets "projector" parameter on True or False, depending on form data.
If there is an error, returns form with infromation for the user about what went wrong.

ModifyRoomView: Modifies objects parameters. On GET returns form with loaded object, on POST does similar things to AddRoomView: checks name, size and set projector. If there is an error it returns form with objects data and information about an error.

RoomReservationView: View made for reservations. On GET returns form with comment and date inputs, and a list of future reservations for given room.
View on POST request checks if date is not taken and not from the past, and saves it. Returns user to main page if everything is alright.

Functions:

There are 3 functions for simple operations in project:

base: Function made for the main page. Returns HTML file with list of rooms, info about them, buttons for reservation, edition and deletion, and if they are reserved for today. Name is a hyperlink to more specific page about the room.

show_room: More specific view for the room. Returns HTML and room object with given id. Shows every information about the room, as well as all of reservations made for it. Does not show reservations from the past. Has reservation, edit and delete buttons

delete: Function for deleting an object. Takes id, calls object from database and delets it.

Models:

There are two models in project: Romms and Reservation. Also, there are two meta classes inside Models.py. One for ordering reservations by date and secon for uniqe together on room_id from reservation and name of room.

Coded in Python. Needed dependencies are:

-> Django, 

-> Psycopg2, 

which are present in added venv "django-venv"

