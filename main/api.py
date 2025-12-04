from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from room.models import Room
from guest.models import Guest
from main.models import Reservation
from django.utils import timezone
from datetime import datetime


def dates_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1


@api_view(['POST'])
def check_availability(request):
    check_in = request.data.get("check_in")
    check_out = request.data.get("check_out")
    room_type = request.data.get("room_type")

    if not all([check_in, check_out]):
        return Response({"error": "check_in и check_out обязательны"}, status=400)

    check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out = datetime.strptime(check_out, "%Y-%m-%d").date()

    rooms = Room.objects.all()
    if room_type:
        rooms = rooms.filter(room_type__iexact=room_type)

    free_rooms = []

    for room in rooms:
        reservations = room.reservation_set.all()
        overlap = any(dates_overlap(r.check_in_date, r.check_out_date, check_in, check_out)
                      for r in reservations)

        if not overlap:
            free_rooms.append({
                "id": room.id,
                "room_number": room.room_number,
                "room_type": room.room_type,
                "price_per_night": float(room.price_per_night),
            })

    return Response({
        "available": len(free_rooms) > 0,
        "free_rooms": free_rooms,
        "total": len(free_rooms),
    })
    

@api_view(['POST'])
def reserve_room(request):
    room_id = request.data.get("room_id")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    phone_number = request.data.get("phone_number")
    check_in = request.data.get("check_in")
    check_out = request.data.get("check_out")

    if not all([room_id, first_name, last_name, email, phone_number, check_in, check_out]):
        return Response({"error": "Не все поля указаны"}, status=status.HTTP_400_BAD_REQUEST)

    check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out = datetime.strptime(check_out, "%Y-%m-%d").date()

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({"error": "Такой комнаты нет"}, status=404)

    for r in room.reservation_set.all():
        if dates_overlap(r.check_in_date, r.check_out_date, check_in, check_out):
            return Response({"error": "Комната занята на эти даты"}, status=409)

    guest = Guest.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        government_id="",
        address="",
    )

    reservation = Reservation.objects.create(
        room=room,
        guest=guest,
        check_in_date=check_in,
        check_out_date=check_out,
    )

    return Response({
        "status": "success",
        "reservation_id": reservation.id,
        "room": room.room_number,
        "check_in": check_in,
        "check_out": check_out
    })
