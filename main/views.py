from datetime import date, datetime
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginator_page(List, num, request):
    paginator = Paginator(List, num)
    page = request.GET.get('page')
    try:
        lt = paginator.page(page)
    except PageNotAnInteger:
        lt = paginator.page(1)
    except EmptyPage:
        lt = paginator.page(paginator.num_page)
    return lt


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = User.objects.filter(username=name)
        if user.count() > 0:
            usr = authenticate(username=name, password=password)
            if usr is not None:
                login(request, usr)
                return redirect('dashboard')
            else:
                return redirect('error_password')
    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


def error_view(request):
    return render(request, '404.html')


def error_password(request):
    return render(request, '404.html')


@login_required(login_url='login')
def add_staff(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            name = request.POST.get('name')
            last_name = request.POST.get('last-name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('cp')
            number = request.POST.get('number')
            status = request.POST.get('status')
            f = 0
            for i in User.objects.all():
                if i.username == username:
                    f += 1
                else:
                    f += 0
            if f == 1:
                print('user is exist')
            elif f == 0:
                if confirm_password == password:
                    User.objects.create_user(
                        username=username, first_name=name,
                        last_name=last_name, password=password,
                        number=number, role=status)
            return redirect('staff')
        else:
            return render(request, 'staff/add-staff.html')
    except Exception as err:
        print(err)


@login_required(login_url='login')
def dashboard_waiter(request):
    usr = request.user
    if usr.role == 2:
        day = date.today()
        order = Order.objects.filter(date__day=day.day, user=usr, done=True)
        closed = Order.objects.filter(done=True, user=usr)
        available = Order.objects.filter(done=False, user=usr)
        free = Order.objects.filter(done=False, user=None)
        total = 0
        for i in order:
            total += i.bill / 100
        total = total * 4
        context = {
            'closed': closed.count(),
            'open': available.count(),
            'free': free.count(),
            'revenue': total
        }
        return render(request, 'dashboard/dashboard-waiter.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def dashboard_manager(request):
    usr = request.user
    if usr.role == 3:
        day = date.today()
        orders = Order.objects.filter(date__month=day.month, done=True)
        total = 0
        for i in orders:
            total += i.bill / 100
        total = total * 8
        context = {
            'salary': total,
            'product': Product.objects.filter(available=True).count(),
            'food': Food.objects.filter(available=True).count(),
            'room': Rooms.objects.all().count()
        }
        return render(request, 'dashboard/dashboard-manager.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def dashboard_cooker(request):
    usr = request.user
    if usr.role == 4:
        day = date.today()
        order = Order.objects.filter(done=True, date__month=day.month)
        close = OrderItem.objects.filter(order__date__day=day.day, done=True)
        usable = OrderItem.objects.filter(order__date__day=day.day, done=False)
        total = 0
        for i in order:
            total += i.bill / 100
            total = total * 3
        context = {
            'salary': total,
            'open': usable.count(),
            'close': close.count(),
        }
        return render(request, 'dashboard/dashboard-cooker.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def dashboard_call_center(request):
    usr = request.user
    if usr.role == 5:
        day = date.today()
        order = Order.objects.filter(done=True, date__month=day.month)
        client = Client.objects.all()
        room = Rooms.objects.filter(busy=False)
        available = Order.objects.filter(done=False, date__day=day.day)
        total = 0
        print(order.count())
        for i in order:
            percent = i.bill / 100
            salary = percent * 1
            if order.count() > 1:
                if salary < 1:
                    salary += 0.000000000000001
            total += salary
        context = {
            'client': client.count(),
            'salary': total,
            'room': room.count(),
            'available': available.count(),
        }
        return render(request, 'dashboard/dashboard-call.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='login')
def dashboard(request):
    usr = request.user
    if usr.role == 1:
        day = date.today()
        client = Client.objects.all().count()
        staff = User.objects.all().count()
        order = Order.objects.filter(done=True, date__month=day.month)
        total = 0
        for i in order:
            total += i.bill
        revenue = total
        percent = total / 100
        three = percent * 3
        four = percent * 4
        five = percent * 5
        eight = percent * 8
        print(eight, five, four, three)
        overall = three + four + five + eight
        print(overall)
        revenue -= int(overall)
        chart = Order.objects.filter(done=True, date__year=day.year)
        jan = [0]
        feb = [0]
        mar = [0]
        apr = [0]
        may = [0]
        june = [0]
        july = [0]
        avg = [0]
        sep = [0]
        ocb = [0]
        nov = [0]
        dec = [0]
        for i in chart:
            if i.date.month == 1:
                jan[0-0] += 1
            elif i.date.month == 2:
                feb[0-0] += 1
            elif i.date.monht == 3:
                mar[0-0] += 1
            elif i.date.month == 4:
                apr[0-0] += 1
            elif i.date.month == 5:
                may[0-0] += 1
            elif i.date.month == 6:
                june[0-0] += 1
            elif i.date.monht == 7:
                july[0-0] += 1
            elif i.date.month == 8:
                avg[0-0] += 1
            elif i.date.month == 9:
                sep[0-0] += 1
            elif i.date.monht == 10:
                ocb[0-0] += 1
            elif i.date.month == 11:
                nov[0-0] += 1
            elif i.date.month == 12:
                dec[0-0] += 1
        context = {
            'client': client,
            'staff': staff,
            'total': total,
            'revenue': revenue,
            'jan': jan,
            'feb': feb,
            'mar': mar,
            'apr': apr,
            'may': may,
            'june': june,
            'july': july,
            'aug': avg,
            'sep': sep,
            'oct': ocb,
            'nov': nov,
            'dec': dec,
        }
        return render(request, 'dashboard/dashboard.html', context)
    elif usr.role == 2:
        return redirect('dashboard-w')
    elif usr.role == 3:
        return redirect('dashboard-m')
    elif usr.role == 4:
        return redirect('dashboard-c')
    elif usr.role == 5:
        return redirect('dashboard-call')
    else:
        return redirect('404')


@login_required(login_url='login')
def manager_view(request):
    usr = request.user
    if usr.role == 1:
        context = {
            'total': User.objects.filter(role=3).count(),
            'manager': paginator_page(User.objects.filter(role=3), 5, request)
        }
        return render(request, 'staff/manager.html', context)
    elif usr.role == 3:
        context = {
            'total': User.objects.filter(role=3).count(),
            'manager': paginator_page(User.objects.filter(role=3), 5, request)
        }
        return render(request, 'staff/manager.html', context)
    else:
        return redirect('404')


@login_required(login_url='login')
def cooker_view(request):
    usr = request.user
    if usr.role == 1:
        context = {
            'total': User.objects.filter(role=4).count(),
            'cooker': paginator_page(User.objects.filter(role=4), 5, request)
        }
        return render(request, 'staff/cooker.html', context)
    elif usr.role == 3:
        context = {
            'total': User.objects.filter(role=4).count(),
            'cooker': paginator_page(User.objects.filter(role=4), 5, request)
        }
        return render(request, 'staff/cooker.html', context)
    else:
        return redirect('404')


@login_required(login_url='login')
def director_view(request):
    user = request.user
    if user.role == 1:
        context = {
            'total': User.objects.filter(role=1).count(),
            'director': paginator_page(User.objects.filter(role=1), 5, request)
        }
        return render(request, 'staff/director.html', context)
    elif user.role == 3:
        context = {
            'total': User.objects.filter(role=1).count(),
            'director': paginator_page(User.objects.filter(role=1), 5, request)
        }
        return render(request, 'staff/director.html', context)
    else:
        return redirect('404')


@login_required(login_url='login')
def waiters_view(request):
    user = request.user
    if user.role == 1:
        context = {
            'total': User.objects.filter(role=2).count(),
            'waiter': paginator_page(User.objects.filter(role=2), 5, request)
        }
        return render(request, 'staff/waiter.html', context)
    elif user.role == 3:
        context = {
            'total': User.objects.filter(role=2).count(),
            'waiter': paginator_page(User.objects.filter(role=2), 5, request)
        }
        return render(request, 'staff/waiter.html', context)
    else:
        return redirect('404')


@login_required(login_url='login')
def call_center_view(request):
    usr = request.user
    if usr.role == 1:
        context = {
            'total': User.objects.filter(role=5).count(),
            'call_center': paginator_page(User.objects.filter(role=5), 5, request)
        }
        return render(request, 'staff/call-canter.html', context)
    elif usr.role == 3:
        context = {
            'total': User.objects.filter(role=5).count(),
            'call_center': paginator_page(User.objects.filter(role=5), 5, request)
        }
        return render(request, 'staff/call-canter.html', context)
    else:
        return redirect('404')


@login_required(login_url='login')
def client_view(request):
    context = {
        'total': Client.objects.all().count(),
        'client': paginator_page(Client.objects.all(), 5, request),
    }
    return render(request, 'staff/client.html', context)


@login_required(login_url='login')
def product_view(request):
    pro = Product.objects.all()
    context = {
        'total': pro.count(),
        'product': paginator_page(pro, 5, request),
        'category': Category.objects.all()
    }
    for i in pro:
        if i.quantity <= 0:
            i.available = False
        else:
            i.available = True
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        if int(quantity) > 0:
            available = True
        elif int(quantity) <= 0:
            available = False
        Product.objects.create(name=name, price=price, quantity=quantity, available=available, category_id=category)
        return redirect('product')
    return render(request, 'product/product.html', context)


@login_required(login_url='login')
def category_view(request):
    context = {
        'total': Category.objects.all().count(),
        'category': paginator_page(Category.objects.all(), 5, request)
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category')
    return render(request, 'product/category.html', context)


@login_required(login_url='login')
def staff_view(request):
    context = {
        'staff': paginator_page(User.objects.all(), 5, request),
        'total': User.objects.all().count()
    }
    return render(request, 'staff/staff.html', context)


@login_required(login_url='login')
def food_view(request):
    context = {
        'category': Category.objects.all(),
        'total': Food.objects.all().count(),
        'food': paginator_page(Food.objects.all(), 5, request)
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        available = request.POST.get('available')
        if available is None:
            available = False
        Food.objects.create(
            name=name, price=price, category_id=category, available=available)
        return redirect('food')
    return render(request, 'product/food.html', context)


@login_required(login_url='login')
def room_view(request):
    context = {
        'total': Rooms.objects.all().count(),
        'room': paginator_page(Rooms.objects.all(), 5, request)
    }
    if request.method == 'POST':
        number = request.POST.get('number')
        place = request.POST.get('place')
        Rooms.objects.create(number=number, places=place)
        return redirect('room')
    return render(request, 'product/room.html', context)


@login_required(login_url='login')
def order_view(request):
    d = date.today()
    order = Order.objects.filter(delivery=False, done=False)
    for i in order:
        if i.date.day == d.day:
            r = Rooms.objects.get(id=i.room.id)
            r.busy = True
            r.save()
    try:
        if request.method == 'POST':
            day = datetime.strptime(request.POST.get('date'), "%m/%d/%Y").date()
            OrderDay.objects.create(day=day)
            return redirect('add-order')
        context = {
            'order': paginator_page(Order.objects.filter(delivery=False), 5, request),
            'food': Food.objects.filter(available=True),
            'product': Product.objects.filter(available=True)
        }
        return render(request, 'product/order.html', context)
    except Exception as err:
        return err


@login_required(login_url='login')
def add_order(request):
    room_list = []
    for i in Rooms.objects.all():
        room_list.append(i)
    for i in Order.objects.all():
        if i.date == OrderDay.objects.last().day:
            room_list.remove(i.room)
    try:
        if request.method == 'POST':
            user = request.POST.get('user')
            room = request.POST.get('room')
            client = request.POST.get('owner')
            phone = request.POST.get('phone')
            day = OrderDay.objects.last().day
            f = 0
            for i in Client.objects.all():
                if i.phone == int(phone):
                    f += 1
                else:
                    f += 0
            if f == 1:
                cl = Client.objects.get(phone=phone)
                Order.objects.create(user_id=user, room_id=room, owner=cl, delivery=False, date=day, bill=0)
                return redirect('order')
            elif f == 0:
                cl = Client.objects.create(name=client, phone=phone)
                Order.objects.create(user_id=user, room_id=room, owner=cl, delivery=False, date=day, bill=0)
                return redirect('order')
        context = {
            'room': room_list,
            'waiter': User.objects.filter(role=2),
        }
        return render(request, 'product/add-order.html', context)
    except Exception as err:
        print(err)


@login_required(login_url='login')
def delivery_view(request):
    d = datetime.today()
    order = Order.objects.filter(delivery_date__hour=d.hour)
    for i in order:
        i.done = True
        i.save()
    context = {
        'delivery': paginator_page(Order.objects.filter(delivery=True), 5, request),
    }
    try:
        if request.method == 'POST':
            user = request.POST.get('user')
            client = request.POST.get('owner')
            phone = request.POST.get('phone')
            day = datetime.strptime(request.POST.get('date'), "%m/%d/%Y").date()
            f = 0
            for i in Client.objects.all():
                if i.phone == int(phone):
                    f += 1
                else:
                    f += 0
            if f == 1:
                cl = Client.objects.get(phone=phone)
                Order.objects.create(user_id=user, owner=cl, delivery=True, date=day, bill=0)
                return redirect('delivery')
            elif f == 0:
                cl = Client.objects.create(name=client, phone=phone)
                Order.objects.create(user_id=user, owner=cl, delivery=True, date=day, bill=0)
                return redirect('order')
        return render(request, 'product/delivery.html', context)
    except Exception as err:
        print(err)


@login_required(login_url='login')
def order_item_view(request):
    day = date.today()
    context = {
        'order': Order.objects.filter(done=False),
        'item': paginator_page(OrderItem.objects.all(), 5, request),
        'product': Product.objects.filter(available=True),
        'food': Food.objects.filter(available=True),
    }
    if request.method == 'POST':
        order = request.POST.get('order')
        food = request.POST.get('food')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        if food == 'Nothing':
            pro = Product.objects.get(id=product)
            if int(quantity) > pro.quantity:
                quantity = pro.quantity
            pro.quantity -= int(quantity)
            pro.save()
            rd = Order.objects.get(id=order)
            rd.bill += pro.price * int(quantity)
            rd.save()
            OrderItem.objects.create(
                order=rd,
                product=pro,
                quantity=quantity)
        elif product == 'Nothing':
            fd = Food.objects.get(id=food)
            rd = Order.objects.get(id=order)
            rd.bill += fd.price * int(quantity)
            rd.save()
            OrderItem.objects.create(
                order=rd,
                food=fd,
                quantity=quantity)
        return redirect('order-item')
    return render(request, 'product/order-item.html', context)


@login_required(login_url='login')
def add_order_item(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        food = request.POST.get('food')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        if food == 'Nothing':
            pro = Product.objects.get(id=product)
            if int(quantity) > pro.quantity:
                quantity = pro.quantity
            pro.quantity -= int(quantity)
            pro.save()
            order.bill += pro.price * int(quantity)
            order.save()
            OrderItem.objects.create(
                order=order,
                product=pro,
                quantity=quantity)
        elif product == 'Nothing':
            fd = Food.objects.get(id=food)
            order.bill += fd.price * int(quantity)
            order.save()
            OrderItem.objects.create(
                order=order,
                food=fd,
                quantity=quantity)
        return redirect('order')
    context = {
        'food': Food.objects.all(),
        'product': Product.objects.all(),
    }
    return render(request, 'product/order.html', context)


@login_required(login_url='login')
def order_item_cooker(request):
    item = OrderItem.objects.all()
    order = []
    for i in item:
        if i.order.done == False:
            order.append(i)
    context = {
        'item': paginator_page(order, 5, request),
    }
    return render(request, 'product/cooker-item.html', context)


@login_required(login_url='login')
def out_of_service_view(request):
    day = date.today()
    context = {
        'orders': Order.objects.filter(done=False, date__day=day.day, user=None)
    }
    return render(request, 'product/unserved-orders.html', context)


@login_required(login_url='login')
def search_user(request):
    if request.method == 'POST':
        total = 0
        username = request.POST.get('username')
        user = User.objects.filter(username=username)
        name = User.objects.filter(first_name=username)
        l_name = User.objects.filter(last_name=username)
        total += user.count()
        total += name.count()
        total += l_name.count()
    result = {
        'usr': user,
        'name': name,
        'l_name': l_name,
        'total': total
    }
    return render(request, 'search.html', result)


@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        total = 0
        name = request.POST.get('name')
        category = Category.objects.filter(name__icontains=name)
        food = Food.objects.filter(name__icontains=name)
        product = Product.objects.filter(name__icontains=name)
        room = Rooms.objects.filter(number__icontains=name)
        total += category.count()
        total += food.count()
        total += product.count()
        total += room.count()
    context = {
        'category': category,
        'food': food,
        'product': product,
        'room': room,
        'total': total
    }
    return render(request, 'product/search.html', context)


@login_required(login_url='login')
def close_items(request):
    return render(request, 'single/close-item.html', {'close': paginator_page(OrderItem.objects.filter(done=True), 5, request)})


@login_required(login_url='login')
def open_items(request):
    return render(request, 'single/open-item.html', {'open': paginator_page(OrderItem.objects.filter(done=False), 5, request)})


@login_required(login_url='login')
def free_room(request):
    return render(request, 'single/free-room.html', {'room': paginator_page(Rooms.objects.filter(busy=False), 5, request)})


@login_required(login_url='login')
def open_order(request):
    context = {
        'product': Product.objects.filter(available=True),
        'food': Food.objects.filter(available=True),
        'order': paginator_page(Order.objects.filter(done=False), 5, request)
    }
    return render(request, 'single/open-order.html', context)

