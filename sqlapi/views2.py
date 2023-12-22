from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Table, Permission, Operations
from rest_framework import status


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def permission(request):
    query=request.data
    if query.get('permission')=="grant":
        return assign_permission(request)
    elif query.get('permission')=="revoke":
        return revoke_permission(request)
    elif query.get('permission')=="check":
        result=get_user_table_permissions(request.user)
        return Response({'result': result}, status=status.HTTP_200_OK)
    else:
        return Response({'result':"intension not clear"},status=status.HTTP_400_BAD_REQUEST)


def assign_permission(request):
    user=request.user
    query=request.data
    prefix=query.get('prefix',"")
    data=query.get('data')
    table=prefix+data.get('table')
    if isTableOwner(user,table):
        action=data.get('action','read')
        userid=data.get('userid',False)
        if userid:
            result=give_permission(table,action,userid)
            return Response({'result': result}, status=status.HTTP_200_OK)
        else:
            username=data.get('username','')
            if(username):
                result =give_permission(table,action,username=username)
                return Response({'result': result}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'please provide userid or username to whom you wanna permit'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'result':"Wait a sec, you are not the owner of this table"}, status=status.HTTP_403_FORBIDDEN)


def revoke_permission(request):
    user=request.user
    query=request.data
    prefix=query.get('prefix',"")
    data=query.get('data')
    table=prefix+data.get('table')
    if isTableOwner(user,table):
        action=data.get('action','read')
        userid=data.get('userid',False)
        if userid:
            if userid==str(user.id): return Response({'result': 'You cant revoke permission yourself'}, status=status.HTTP_400_BAD_REQUEST) 
            result=remove_permission(table,action,userid)
            return Response({'result': result}, status=status.HTTP_200_OK)
        else:
            username=data.get('username','')
            if(username):
                if username==user.username: return Response({'result': 'You cant revoke permission yourself'}, status=status.HTTP_400_BAD_REQUEST) 
                result =remove_permission(table,action,username=username)
                return Response({'result': result}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'please provide userid or username to whom you wanna remove'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'result':"Wait a sec, you are not the owner of this table"}, status=status.HTTP_403_FORBIDDEN)

def isTableOwner(user,table):
    try:
        Table.objects.get(table_name=table, creator=user)
        return True
    except Table.DoesNotExist:
        return False


def doesHavePermissionOfAction(user, table_name, action):
    try:
        read_operation = Operations.objects.get(opTitle=action)
        _ = Permission.objects.get(user=user, operation=read_operation, table__table_name=table_name)
        return True
    except Permission.DoesNotExist:
        return False
    
def give_permission(tablename, action,userid='',username=''):
    if userid:
        user = User.objects.get(id=userid)
    if username:
        user = User.objects.get(username=username)
        
    table = Table.objects.get(table_name=tablename)
    operation= Operations.objects.get(opTitle=action)
    permission, created = Permission.objects.get_or_create(user=user, table=table, operation=operation)
    return 'permission granted for '+action if created else 'permission already granted'

def remove_permission(tablename, action, userid='', username=''):
    try:
        if userid:
            user = User.objects.get(id=userid)
        elif username:
            user = User.objects.get(username=username)
        else:
            raise ValueError("Please provide either userid or username.")

        table = Table.objects.get(table_name=tablename)
        operation = Operations.objects.get(opTitle=action)

        permission = Permission.objects.get(user=user, table=table, operation=operation)
        permission.delete()

        return f'Permission revoked for {action}'
    except User.DoesNotExist:
        return 'User not found'
    except Table.DoesNotExist:
        return 'Table not found'
    except Operations.DoesNotExist:
        return 'Operation not found'
    except Permission.DoesNotExist:
        return 'Permission not found'



def get_user_table_permissions(current_user):
    user_permissions = {}
    user_tables = Table.objects.filter(creator=current_user)
    for table in user_tables:
        table_name = table.table_name
        user_permissions[table_name] = {}
        table_permissions = Permission.objects.filter(table=table)
        for permission in table_permissions:
            other_user = permission.user
            if other_user != current_user:
                if other_user.username not in user_permissions[table_name]:
                    user_permissions[table_name][other_user.username] = []
                user_permissions[table_name][other_user.username].append(permission.operation.opTitle)
    return user_permissions