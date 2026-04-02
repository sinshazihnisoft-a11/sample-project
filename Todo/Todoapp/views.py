
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from Todoapp.models import Todo_item
from Todoapp.serializer import Todo_item_serializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from .permissions import IsOwnerPermission


# Create your views here.
class Todo_item_view(ListAPIView):
    serializer_class = Todo_item_serializer
    model_name = Todo_item

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        print("request user:", self.request.user)
        qs = self.model_name.objects.filter(created_by= self.request.user)
        return qs
    
    def post(self, request):
        print("request:", request.data)
        id = request.data.get("id")
        message = ""

        if id:

            Todo_obj = self.model_name.objects.get(id=id)
            serializer_obj = self.serializer_class(Todo_obj, data= request.data)
            message = "Updated successfully"
            
        else:
            serializer_obj = self.serializer_class(data= request.data)
            message = "Created successfully"


        serializer_obj.is_valid(raise_exception= True)
        serializer_obj.save(created_by= self.request.user)

        return Response(
            {
                'message': message,
                'data': serializer_obj.data
            }
        )
    
   
    def delete(self, request):
        id = request.GET.get('id')
        print("id:", id)
        self.model_name.objects.filter(id=id).delete()

        return Response(
            {
                'message': 'deleted successfully'
            }
        )
    
class UserRegisterAPIView(ListAPIView):
    def post(self,request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')

        user_obj = User.objects.create_user(username = username, password = password)
        user_obj.save()
        return Response(
            {
                'message' : 'User created successfully'
            }
        )
    

class LoginAPIView(ListAPIView):
    def post(self, request):
        try:
            username = self.request.data.get('username')
            password = self.request.data.get('password')

            user_obj = User.objects.filter(username = username).first()
            is_valid =  user_obj.check_password(password)

            if is_valid:
               token_obj, is_created = Token.objects.get_or_create(user=user_obj)
               print("token_obj:", token_obj.key)
               print("token_obj:", is_created)
               return Response(
                   {
                       'message' : 'Login successfully',
                       'token' : f'Token {token_obj.key}'
                   }
               )
                

    
            print("is_invalid:", is_valid)
            return Response(
                {
                    'message': 'invalid credentials'
                }
            )
        
        except User.DoesNotExist:
            return Response(
                {
                    'message' : 'invalid credentials'
                }
            )
        except Exception as e:
            return Response(
                {
                    'message' : str(e)
                }
            )
        
class LogoutAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            user = request.user
            token, created = Token.objects.get_or_create(user=user)
            token.delete()
            return Response(
                {
                    'message' : 'Logged out successfully'
                }
            )
        except User.DoesNotExist:
            return Response(
                {
                    'message' : 'Invalid credentials'
                }
            )
        except Exception as e:
            return Response(
                {
                    'message' : str(e)
                }
            )
       