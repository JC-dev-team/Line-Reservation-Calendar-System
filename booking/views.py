from datetime import datetime
from django.shortcuts import render, redirect, reverse
from .models import ActionLog, BkList, Account, Production, Staff, Store
from .serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from . import auth
from django.db import transaction, DatabaseError
from django.db.models import Q  # complex lookup
# from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import login_required
# ----- Class site ----------------------


class ActionLogViewSet(viewsets.ModelViewSet):
    queryset = ActionLog.objects.all()
    serializer_class = Actlog_Serializer


class BkListViewSet(viewsets.ModelViewSet):
    queryset = BkList.objects.all()
    serializer_class = Bklist_Serializer


class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = Prod_Serializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = Store_Serializer
    permission_classes = (IsAuthenticated,)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = Staff_Serializer

# admin dashboard -------------------


def staff_login(request):  # authentication staff
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        result = auth.StaffAuthentication(social_id, social_app)

        if result == None or result == False:
            return render(request, 'error/error404.html')

        elif list(result.keys())[0] == 'error':  # error occurred
            return render(request, 'error/error.html', {'error': result['error']})
        else:
            return render(request, 'admin_dashboard.html', {'data': result})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def staff_checkbooking(request):
    try:
        store_id = request.POST.get('store_id', None)
        bk_date = request.POST.get('bk_date', None)

        pass
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def staff_approval_booking(request):
    try:
        bk_id = request.POST.get('bk_id', None)
        pass
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


class AccountViewSet(viewsets.ModelViewSet):  # api get account data
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer

    def get_queryset(self):
        queryset = self.queryset
        phone = self.request.query_params.get('phone', None)
        social_id = self.request.query_params.get('social_id', None)

        query_set = queryset.filter(phone=phone)
        return query_set

# Definition site ------------------------------------------------


def ToBookingView(request):  # The member.html via here in oreder to enroll new member
    try:
        phone = request.POST.get('phone', None)
        username = request.POST.get('username', None)
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        with transaction.atomic():  # transaction
            queryset = Account.objects.create(
                phone=phone,
                username=username,
                social_id=social_id,
                social_app=social_app,
            )
            queryset = Account.objects.select_for_update().get(
                phone=phone,
                username=username,
                social_id=social_id,
                social_app=social_app
            )

        serializer_class = Acc_Serializer(queryset)
        # render html
        return render(request, 'reservation.html', {'data': serializer_class.data})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})  # render html


def booking_list(request):  # the booking list
    try:
        user_id = request.POST.get('user_id', None)
        store_id = request.POST.get('store_id', None)
        bk_date = request.POST.get('bk_date', None)
        bk_st = request.POST.get('bk_st', None)
        bk_ed = request.POST.get('bk_ed', None)
        adult = request.POST.get('adult', None)
        children = request.POST.get('children', None)
        bk_ps = request.POST.get('bk_ps', None)
        event_type = request.POST.get('event_type', None)
        time_session = request.POST.get('time_session', None)
        entire_time = request.POST.get('entire_time', False)
        is_cancel = False
        waiting_num = 0
        total = int(adult)+int(children)
        exact_seat = 0

        with transaction.atomic():  # transaction
            # get the store seat
            store_query = Store.objects.only('seat').select_for_update().get(
                store_id=store_id
            )
            if store_query.seat < total:
                raise Exception('超過總容納人數')
            # get the booking event of that time session
            bk_queryset = BkList.objects.select_for_update().filter(
                store_id=store_id,
                bk_date=bk_date,
                time_session=time_session,
                is_cancel=is_cancel,
            )

            # count is that enough for seat values
            for i in bk_queryset:
                number = int(i.adult)+int(i.children)
                exact_seat += number

            if (exact_seat+total) > store_query.seat:
                return render(request, 'reservation.html', {'error': '人數過多'})

            else:
                # get waiting_num
                waiting_num = BkList.objects.only('waiting_num').select_for_update().filter(
                    store_id=store_id,
                    bk_date=bk_date,
                    time_session=time_session,
                    is_cancel=is_cancel,
                ).count()
                waiting_num += 1
                final_queryset = BkList.objects.create(  # insert data
                    user_id=user_id,
                    store_id=store_id,
                    bk_date=bk_date,
                    bk_st=bk_st,
                    bk_ed=bk_ed,
                    adult=adult,
                    children=children,
                    bk_ps=bk_ps,
                    event_type=event_type,
                    time_session=time_session,
                    entire_time=entire_time,
                    is_cancel=is_cancel,
                    waiting_num=waiting_num,
                )
                # request.session.flush()
                serializer_class = Bklist_Serializer(final_queryset)
                return render(request, '', {'data': serializer_class.data})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def login_portal(request):
    return render(request, 'login.html',)


def reservation(request):
    return render(request, 'reservation.html')


def test_check_reservation(request):
    return render(request, 'test_check_reservation.html')


def member(request):
    try:  # Check Login
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        result = auth.ClientAuthentication(
            social_id, social_app)  # queryset or something else
        if result == None:  # Using PC or No social login
            return redirect('/booking/login/',)
        elif result == False:  # Account Not Exist
            return render(request, 'member.html',)
            # return redirect(reverse('member'),args=())
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            return render(request, 'error/error.html', {'error': result['error']})
        else:  # Account Exist
            serializer = Acc_Serializer(result)
            request.session['member_id'] = result.user_id
            return render(request, 'reservation.html', {'data': serializer.data})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def check_reservation(request):
    try:
        store_id = request.POST.get('store_id', None)
        # bk_date = request.POST.get('bk_date',None)
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)

        acc_queryset = Account.objects.only('user_id').get(
            social_id=social_id,
            social_app=social_app,
        )
        queryset = BkList.objects.filter(
            user_id=acc_queryset.user_id,
            store_id=store_id,
        )

        serializer = Acc_Serializer(queryset)
        return render(request, 'check_reservation.html', {'data': serializer.data})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})

# Ajax api -------------------------------------------------------------- 
def getCalendar(request):
    try:
        store_id = request.POST.get('store_id', None)
        start_month = request.POST.get('start_month', None)
        end_month = request.POST.get('end_month', None)
        adults = request.POST.get('adults', None)
        children = request.POST.get('children', None)

        # Convert string to time
        start_month = datetime.strptime(start_month, '%Y-%m-%d').date()
        end_month = datetime.strptime(end_month, '%Y-%m-%d').date()
        # The days between start and end
        # days = (end_month-start_month).days()

        store_query = Store.objects.only('seat').select_for_update().get(
            store_id=store_id
        )

        bookinglist = BkList.objects.filter(
            store_id=store_id,
            bk_date__range=(start_month, end_month),
            is_cancel=False,
            waiting_num=0,
        )
        event_arr = []
        for i in bookinglist:
            event_sub_arr = {}  # event dictionary noon
            if i.entire_time == True:
                event_sub_arr['title'] = i.time_session+i.event_type
                event_sub_arr['start'] = i.bk_st
                event_sub_arr['backgroundColor'] = 'red'
            elif int(i.adult)+int(i.children)+int(adults)+int(children) > store_query.seat:
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.bk_st
                event_sub_arr['backgroundColor'] = 'red'
            else:
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.bk_st
                event_sub_arr['backgroundColor'] = 'green'
            event_sub_arr['textColor'] = 'white'
            event_arr.append(event_sub_arr)

        return JsonResponse(event_arr)
    except Exception as e:
        return JsonResponse({'error': e})


# Test function ------------------------
def testtemplate(request):
    return render(request, 'test/test.html')


class testView(APIView):  # render html
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None

    def post(self, request, format=None):
        try:
            self.template_name = 'booking.html'
            with transaction.atomic():  # transaction
                serializer = Acc_Serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': request.data}, status=status.HTTP_201_CREATED)
                else:
                    self.template_name = 'error/error.html'
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.template_name = 'error/error.html'
            return Response({'error': e})
