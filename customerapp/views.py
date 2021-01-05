from django.shortcuts import render
from .serializers import AddressSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Addresses
from db_utils.connect import dictfetchone, dictfetchall
from django.db import connection


class GetUserAddress(APIView):
  """Get user addresses"""
  permission_classes = [permissions.IsAuthenticated,]

  def get(self, request, id, format=None):
    """get user addresses"""
    addresses = Addresses.objects.filter(userid = id)
    if addresses:
      serializer = AddressSerializer(addresses, many = True)
      return Response(serializer.data)  
    else:
      return Response(status = status.HTTP_404_NOT_FOUND)


class AddUserAddress(APIView):
  """Add user addresses"""
  permission_classes = [ permissions.IsAuthenticated, ]

  def post(self, request, format=None):
    serializer = AddressSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save(userid=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserAddress(APIView):
  """Edit user address""" 
  permission_classes = [ permissions.IsAuthenticated, ]

  def put(self, request, id, format=None):
    try:
      instance = Addresses.objects.get(pk=id)
    except Addresses.DoesNotExist:
      return Response({'msg':'No address found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AddressSerializer(instance, data = request.data, partial=True)
    if serializer.is_valid():
      addr = serializer.save()
      return Response({'addr': AddressSerializer(addr).data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAddress(APIView):
  """Delete user addresses"""
  permission_classes = [ permissions.IsAuthenticated, ]

  def post(self, request, addrId, format=None):
    with connection.cursor() as cur:
      cur.execute('select * from customerapp_addresses where id = %s', [addrId])
      if cur.rowcount == 1:
        cur.execute('delete from customerapp_addresses where id = %s', [addrId])
        return Response({"msg":"Address deleted"}, status = status.HTTP_200_OK)
      else:
        return Response({"msg":"Address not found"}, status = status.HTTP_404_NOT_FOUND)


class UpdateActiveAddress(APIView):
  """Update active address of a user"""
  permission_classes = [ permissions.IsAuthenticated, ]
  
  def put(self, request, addrId, format=None):
    with connection.cursor() as cur:
      cur.execute('select * from customerapp_addresses where userid_id =\
                  %s',[request.user.id])
      addresses = dictfetchall(cur)
      for add in addresses:
        if add['is_active'] == True:
          cur.execute('update customerapp_addresses set is_active = %s \
                where id = %s', [False, add['id']])
      cur.execute('update customerapp_addresses set is_active = %s where \
              id = %s', [True, addrId])

    return Response({'msg':'Active address updated'}, status=status.HTTP_200_OK)


