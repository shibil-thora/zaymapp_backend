from rest_framework.views import APIView 
from rest_framework import status  
from .razorpay_serializers import CreateOrderSerializer, TransactionSerializer
from rest_framework.response import Response 
from .razorpay.main import RazorPayClient  
from django.conf import settings
from ..models import Transaction
from rest_framework.permissions import IsAuthenticated 
from users.models import MyUsers as User

rz_client = RazorPayClient()


class CreateOrderAPIView(APIView): 
    def post(self, request): 
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid(): 
            order_response = rz_client.create_order(
                amount=create_order_serializer.validated_data.get("amount"),
                currency=create_order_serializer.validated_data.get("currency"),
            )
            response = {
                "status_code": status.HTTP_201_CREATED, 
                "message": "order_created", 
                "data": order_response,  
                # here you are providing the razorpay secret key to the frontend
                "key": settings.RAZORPAY_KEY_ID, 
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else: 
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST, 
                "message": "bad request", 
                "error": create_order_serializer.errors, 
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView): 
    def post(self, request): 
       
        rz_client.verify_payment(
            razorpay_order_id=request.data.get("order_id"), 
            razorpay_payment_id=request.data.get("payment_id"), 
            razorpay_signature=request.data.get("signature"), 
        ) 
        user_obj = User.objects.get(username=request.data.get("user"))
        Transaction.objects.create(
            user=user_obj,
            payment_id=request.data.get("payment_id"),
            order_id=request.data.get("order_id"),
            signature=request.data.get("signature"),
            amount=request.data.get("amount"),
        )
        user_obj.is_premium = True 
        user_obj.save()

        response = {
            "status_code": status.HTTP_201_CREATED, 
            "message": "transaction created", 
        }
        return Response(response, status=status.HTTP_201_CREATED)
         