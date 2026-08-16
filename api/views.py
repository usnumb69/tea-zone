from.serializer import *
from main.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, datetime




class Get_product(APIView):
    def get(self, request):
        product = Product.objects.filter(available=True)
        products = []
        for i in product:
            data = {
                'name': i.name,
                'price': i.price,
                'category': i.category

            }
            products.append(data)
        return Response(products)


class Get_food(APIView):
    def get(self, request):
        food = Food.objects.filter(available=True)
        foods = []
        for i in food:
            data = {
                'name': i.name,
                'price': i.price,
                'category': i.category

            }
            foods.append(data)
        return Response(foods)


@api_view(['POST'])
def get_rooms(request):
    date = request.POST['date']
    order = Order.objects.filter(done=False, date=date)
    room = []
    busy = []
    if order:
        for x in Rooms.objects.all():
            for i in order:
                if x == i.room:
                    busy.append(x)
                else:
                    if x in room:

                        pass
                    else:

                        room.append(x)
        for i in busy:
            if i in room:
                room.remove(i)
    else:
        for i in Rooms.objects.filter(busy=False):
            room.append(i)
    return Response(Rooms_serializer(room, many=True).data)


@api_view(['POST'])
def client_create(request):
    name = request.POST.get('name')
    number = request.POST.get('number')
    Client.objects.create(name=name, number=number)
    return Response('')


@api_view(['POST'])
def create_order(request, day=date.today()):
    try:
        day = day
        name = request.POST.get("name")
        room = request.POST.get('room')
        phone = request.POST.get('phone')
        month = request.POST.get("date")
        print(month)
        print(day)
        if Client.objects.filter(phone=phone).count() == 0:
            client = Client.objects.create(name=name, phone=phone)
        else:
            client = Client.objects.get(phone=phone)
        r = Rooms.objects.get(number=room)
        if month == day:
            r.busy = True
        else:
            r.busy = False
        r.save()
        Order.objects.create(
            room=Rooms.objects.get(number=room),
            delivery=False,
            owner=client,
            date=month,
            bill=0
        )
        return Response({"status": 200})
    except Exception as err:
        return Response({"status": 500})


@api_view(['POST'])
def create_delivery(request):
    try:
        name = request.POST.get("name")
        phone = request.POST.get('phone')
        date = request.POST.get("date")
        print(name)
        if Client.objects.filter(phone=phone).count() == 0:
            client = Client.objects.create(name=name, phone=phone)
        else:
            client = Client.objects.get(phone=phone)
        print('else')
        Order.objects.create(
            delivery=True,
            owner=client,
            delivery_date=date,
            bill=0
        )
        print('zurrr')
        return Response({"status": 200})
    except Exception as err:
        print(err)
        return Response({"status": 500})


@api_view(['GET'])
def get_info(request):
    info = Bot.objects.last()
    return Response(BotInfoSerializer(info).data)


@api_view(['GET'])
def get_detail(request):
    info = BotDetail.objects.last()
    return Response(BotDetailSerializer(info).data)






