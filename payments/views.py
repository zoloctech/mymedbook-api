import json
import razorpay
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_payment(request):
    # request.data is coming from frontend
    user = request.user
    amount = request.data['amount']
    # setup razorpay client
    client = razorpay.Client(auth=("rzp_live_4kcfv9AiUdpvbG", "YlX3ZXnPMoj2C2dNylRXhAGO"))
    # create razorpay order
    payment = client.order.create({"amount": int(amount) * 100,"currency": "INR","payment_capture": "1"})
    # we are saving an order with isPaid=False
    order = Order.objects.create(user=user, order_amount=amount, order_payment_id=payment['id'])
    serializer = OrderSerializer(order)
    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response({
        "message": "Payment started successfully",
        "status": status.HTTP_200_OK,
        "success": True,
        "resonse": data
    })

# callback url for razorpay
@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivGft5Lx7I9e',
    'razorpay_order_id': 'order_G3NhGHF655UfjQ',
    'razorpay_signature': '76b2accbefde6cd2392b5njn7sj8ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(
        auth=("rzp_live_4kcfv9AiUdpvbG", "YlX3ZXnPMoj2C2dNylRXhAGO"))

    # checking if the transaction is valid or not if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)
