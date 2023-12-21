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
def assign_permission(request):
    user=request.user
    query=request.data
    prefix=query.get('prefix',"")
    data=query.get('data')
    table=prefix+data.get('table')
    if doesHavePermissionOfAction(user,table,'__all__'):
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


'''
{
    "prefix": "generic",
    "data": {
        "table": "table1",
        "toid":"user_id",
        "toname":"username",
        "action":"read,insert,update,delete"
    }
}


    "action":"assign_permission",
'''