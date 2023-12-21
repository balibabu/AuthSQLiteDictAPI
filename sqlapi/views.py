from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .sqlitedictionary import SQLiteDictDB
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Table, Permission, Operations
import os

sqlDict=SQLiteDictDB()
sqlDict.set_file('constant')

@api_view(['POST'])
def execute_sql(request):
    try:
        query = request.data
        command=query.get('command')
        print(command)
        with connection.cursor() as cursor:
            cursor.execute(command)
            result = cursor.fetchall()
            return Response({"result": result}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sql_dictionary(request):
    user=request.user

    query=request.data
    action=query.get('action')
    prefix=query.get('prefix',"")

    if action=='get_table_names':
        tables=get_user_tables(user)
        return Response({'result':tables}, status=status.HTTP_200_OK)

    data=query.get('data')
    table=prefix+data.get('table')
    sqlDict.set_table_name(table)

    if action=='get_keys':
        if doesHavePermissionOfAction(user,table,'__all__') or doesHavePermissionOfAction(user,table,'read'):
            return Response({'result':sqlDict.get_keys()}, status=status.HTTP_200_OK)
        return Response({'result':"I dont think you have permission"}, status=status.HTTP_403_FORBIDDEN)
    
    if action=='get_content_as_dict':
        if doesHavePermissionOfAction(user,table,'__all__') or doesHavePermissionOfAction(user,table,'read'):
            result=sqlDict.get_content_as_dict()
            return Response({'result':result}, status=status.HTTP_200_OK)
        return Response({'result':"I dont think you have permission"}, status=status.HTTP_403_FORBIDDEN)
    
    if action=='deleteTable':
        if doesHavePermissionOfAction(user,table,'__all__'):
            sqlDict.deleteTable(table)
            return Response({'result':"table deletd successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'result':"I dont think you have permission"}, status=status.HTTP_403_FORBIDDEN)
        
    key=data.get('key')

    if action=='read':
        if doesHavePermissionOfAction(user,table,'__all__') or doesHavePermissionOfAction(user,table,'read'):
            return Response({'result':sqlDict.read(key)}, status=status.HTTP_200_OK)
        return Response({'result':"I dont think you have permission"}, status=status.HTTP_403_FORBIDDEN)
    
    if action=='has':
        if doesHavePermissionOfAction(user,table,'__all__') or doesHavePermissionOfAction(user,table,'read'):
            return Response({'result':sqlDict.has(key)}, status=status.HTTP_200_OK)
        return Response({'result':"I dont think you have permission"}, status=status.HTTP_403_FORBIDDEN)
    
    if action=='delete':
        if doesHavePermissionOfAction(user,table,'__all__') or doesHavePermissionOfAction(user,table,'delete'):
            sqlDict.delete(key)
            return Response({'result':"deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'result':"I dont think you have permission"}, status=status.HTTP_403_FORBIDDEN)

    value=data.get('value')
    if action=='override':
        result= override(user,table,key,value)
        return Response({'result':result}, status=status.HTTP_200_OK)
    return Response({'result':"your action is not right"}, status=status.HTTP_200_OK)

def override(user,table,key,value):
    if not os.path.exists("constant") or table not in sqlDict.get_table_names():
        create_table(user,table)
        sqlDict.override(key,value)
        return "Table Created and value inserted"
    else:
        if doesHavePermissionOfAction(user,table,'__all__') or doesHavePermissionOfAction(user,table,'update') or doesHavePermissionOfAction(user,table,'insert'):
            sqlDict.override(key,value)
            return "Inserted Successfully"
        else:
            return "Table Already Exits and You Dont Have Permission to override"

def create_table(user, table_name):
    new_table = Table.objects.create(creator=user, table_name=table_name)
    new_table.save()

    all_operations = Operations.objects.get(opTitle="__all__")
    Permission.objects.create(user=user, operation=all_operations, table=new_table)

def get_user_tables(user):
    # Retrieve the tables for which the user has permissions
    user_permissions = Permission.objects.filter(user=user).select_related('table', 'operation')

    # Create a list of dictionaries with "table_name" and "permit" keys
    table_permissions = [
        {"table_name": permission.table.table_name, "permit": permission.operation.opTitle}
        for permission in user_permissions
    ]

    return table_permissions

def doesHavePermissionOfAction(user, table_name, action):
    try:
        read_operation = Operations.objects.get(opTitle=action)
        _ = Permission.objects.get(user=user, operation=read_operation, table__table_name=table_name)
        return True
    except Permission.DoesNotExist:
        return False
