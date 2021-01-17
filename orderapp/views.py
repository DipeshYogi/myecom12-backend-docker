from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import OrderSerializer, OrderInfoSerializer, \
                         OrderLineSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from db_utils.connect import dictfetchall, dictfetchone
from datetime import date
from django.db import connection, transaction
from .models import ECH, ECL


class CreateOrder(APIView):
  """Create Order for Customer"""
  permission_classes = [ permissions.IsAuthenticated, ]

  @transaction.atomic
  def post(self, request, format=None):
    serializer = OrderSerializer(data= request.data)
    if serializer.is_valid():
      cust = serializer.data['HCUST']
      shop = serializer.data['HSHOP']
      item =serializer.data['HPROD']

      with connection.cursor() as cur:
        # fetch new order number
        cur.execute("""select max("HORD") from orderapp_ech""")
        try:
          new_ord = dictfetchone(cur)['max'] + 1
        except:
          new_ord = 1
        
        # fetch shop name
        cur.execute("""select "shop_name" from shopkeeperapp_shopprofile where shopid_id \
                    = %s """, [shop])
        shop_name = dictfetchone(cur)['shop_name']

        # write data to ECH order header
        cur.execute("""insert into orderapp_ech("HORD", "HEDTE", "HSTS", "HCUST", "HSHOP", "HSNME") \
                   values (%s,%s,%s,%s,%s,%s)""", [new_ord, date.today(), 'ONGOING', cust, shop, shop_name])

        # write data to ECL order lines
        line = 0
        for i in item:
          line += 1
          cur.execute("""insert into orderapp_ecl("LORD", "LLINE", "LPROD", "LQORD", "LPRIC",\
                      "LDISC") values(%s, %s, %s, %s, %s, %s)""", [new_ord, line, i['name'], \
                      i['quantity'], i['price'], i['discount']])
        
        
      return Response({"msg":"Order_created"}, status=status.HTTP_201_CREATED)
    
    return Response(status= status.HTTP_400_BAD_REQUEST)


class GetUserOrders(APIView):
  """Fetch all user orders"""
  permission_classes = [ permissions.IsAuthenticated, ]

  def get(self, request, format=None):
    with connection.cursor() as cur:
      cur.execute(""" select * from orderapp_ech where "HCUST" = %s """, [request.user.id])
      order_header = dictfetchall(cur)
      orders = []
      for i in order_header:
        orders.append(i["HORD"])      
      cur.execute(""" select * from orderapp_ecl where "LORD" in %s """, (tuple(orders),))
      order_lines = dictfetchall(cur)

    return Response({"HeaderInfo":order_header, "LineInfo":order_lines}, status=status.HTTP_200_OK)


class GetShopOrderHeader(GenericAPIView):
  """
    Fetch Order Header info for the shopkeeper
  """
  serializer_class = OrderInfoSerializer
  permission_classes = [permissions.IsAuthenticated,]

  def get(self, request):
    order_header = ECH.objects.filter(HSHOP = request.user.id)
    if order_header:
      order_data = self.serializer_class(order_header, many = True)
      return Response(order_data.data, status = status.HTTP_200_OK)
    else:
      return Response(status = status.HTTP_404_NOT_FOUND)


class GetShopOrderLines(GenericAPIView):
  """
    Fetch Order Line info for the shopkeeper
  """  
  serializer_class = OrderLineSerializer
  permission_classes = [permissions.IsAuthenticated,]

  def get(self, request, id):
    order_lines = ECL.objects.filter(LORD = id)
    if order_lines:
      order_lines = self.serializer_class(order_lines, many=True)
      return Response(order_lines.data, status = status.HTTP_200_OK)
    else:
      return Response(status.HTTP_404_NOT_FOUND)


class CompleteOrder(GenericAPIView):
  """
    Update Order to completed
  """
  permission_classes = [permissions.IsAuthenticated,]

  def put(self, request, id):
    with connection.cursor() as cur:
      cur.execute(""" select * from orderapp_ech where "HORD" = %s """, [id])
      if cur.rowcount > 0:
        cur.execute(""" update orderapp_ech set "HSTS" = %s where "HORD" = \
                    %s """, ["COMPLETED", id])
        return Response(status = status.HTTP_200_OK)
      else:
        return Response(status = status.HTTP_404_NOT_FOUND)

class CancelOrder(GenericAPIView):
  """
    Update Order to Cancelled
  """
  permission_classes = [permissions.IsAuthenticated,] 

  def put(self, request, id):
    with connection.cursor() as cur:
      cur.execute(""" select * from orderapp_ech where "HORD" = %s """, [id])
      if cur.rowcount > 0:
        cur.execute(""" update orderapp_ech set "HSTS" = %s where "HORD" = \
                    %s """, ["CANCELLED", id])
        return Response(status = status.HTTP_200_OK)
      else:
        return Response(status = status.HTTP_404_NOT_FOUND)



      
