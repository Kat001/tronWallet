from vod.models import Course, CourseEnrollment, EnrollmentTransaction, Student
from django.http.response import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.conf import settings
import razorpay
from django.shortcuts import render


class RazorpayCreateOrder(APIView):
    def post(self, request):
        rz_client = razorpay.Client(
            auth=(settings.RZ_KEY_ID, settings.RZ_KEY_SECRET))
        rz_client.set_app_details(
            {"title": "ArtistSchool_Django", "version": "0.1-alpha"})
        order_amount = 49900  # Razorpay API wants Rs. 499.00 to be written as 49900
        from random import randint
        order_receipt = f'reciept_{randint(0,10**6)}'
        # TODO: Add proper details in notes
        # TODO: Take course slug through query string
        notes = {'studentEmail': 'student@gmail.com'}
        response = rz_client.order.create({
            'amount': int(order_amount),
            'currency': 'INR',
            'payment_capture': '0',
            "notes": notes
        })

        student = Student.objects.first()  # TODO
        course = Course.objects.first()  # TODO

        order_id = response['id']
        order_status = response['status']
        context = {
            'key': settings.RZ_KEY_ID,
            "order_id": order_id,
            "prod_name": course.name,
            "callback_url": "http://localhost:8000/v1/payment/callback/",
            "currency": "INR",
            "amount": str(order_amount),
        }
        try:
            enrollment = CourseEnrollment.objects.get(
                student=student, course=course)
        except:
            enrollment = CourseEnrollment(student=student, course=course)
            enrollment.save()

        transaction = EnrollmentTransaction(
            enrollment=enrollment, razorpay_order_id=order_id)
        transaction.save()

        if order_status == 'created':
            # return render(request, 'pay.html', context)
            return JsonResponse(context)
        else:
            return HttpResponse("ERROR")


class RazorpayCallback(APIView):

    def post(self, request):
        data = request.data
        data = {
            "razorpay_payment_id": data.get("razorpay_payment_id"),
            "razorpay_order_id": data.get("razorpay_order_id"),
            "razorpay_signature": data.get("razorpay_signature")
        }

        transaction = EnrollmentTransaction.objects.get(
            razorpay_order_id=data['razorpay_order_id'])
        transaction.razorpay_payment_id = data['razorpay_payment_id']
        transaction.razorpay_signature = data['razorpay_signature']

        rz_client = razorpay.Client(
            auth=(settings.RZ_KEY_ID, settings.RZ_KEY_SECRET))
        rz_client.set_app_details(
            {"title": "ArtistSchool_Django", "version": "0.1-alpha"})
        try:
            rz_client.utility.verify_payment_signature(data)
            transaction.is_verified = True
        except:
            print("Verification Failed")
        transaction.enrollment.is_enabled = True
        transaction.save()
        transaction.enrollment.save()

        return HttpResponse("Hello World !")
