from operator import ge
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from item.models import Item, Comment
from blog.models import Post

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import *
from .permissions import *


#--------------------------------------------------------------------
#-------------------------Item---------------------------------------
#--------------------------------------------------------------------
class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.filter(status="p")
    serializer_class = ItemListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    permission_classes = [AllowAny,]


class ItemRetrieveAPIView(APIView):

    permission_classes = [IsOwnerOrSuperuserOrReadonly]

    def get_object(self):
        item = get_object_or_404(
            Item,
            pk=self.kwargs['pk']
        )
        return item

    # details of item
    def get(self, request, *args, **kwargs):
        if self.get_object().status == "d":
            return Response({"message":"به اين محصول دسترسي نداريد"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ItemDetailSerializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #update item
    def put(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = ItemSerializerUpdate(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # remove item
    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Add to basket
    def post(self, request, *args, **kwargs):
        orderitem_serializer = OrderItemSerializer(data=request.data)
        if orderitem_serializer.is_valid():
            count = orderitem_serializer.validated_data['count']
            # can't add zero item
            if count == 0:
                return Response({"message":"صفر تعداد انتخاب كرده ايد"}, status=status.HTTP_400_BAD_REQUEST)
            # Selected number of item more than inventory of item
            elif count > self.get_object().inventory:
                return Response({"message":"بيش از حد ظرفيت موجود"}, status=status.HTTP_400_BAD_REQUEST)
            # can't add own item
            elif request.user == self.get_object().company:
                return Response({"message":"اين محصول شماست نمي توانيد به سبد خود اضافه كنيد"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            try:
                update_orderitem  = OrderItem.objects.get(item=self.get_object())
            # if user has not object of order item, create that
            except OrderItem.DoesNotExist:
                new_orderitem = OrderItem.objects.create(
                    item=self.get_object(),
                    count=count,
                    customer=request.user,
                )
                new_orderitem.save()
            else:
                update_orderitem.count += count
                update_orderitem.save()
            
            try:
                upate_order = Order.objects.get(user=request.user)
            # if user has not object of order, create that
            except Order.DoesNotExist:
                new_order = Order.objects.create(
                    user=request.user,
                )
                new_order.save()
                new_order.items.add(OrderItem.objects.get(item=self.get_object()))
            else:
                upate_order.items.add(OrderItem.objects.get(item=self.get_object()))
            return Response({"message":"به سبد اضافه شد"}, status=status.HTTP_200_OK)
        else:
            serializer = OrderItemSerializer()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ItemCreateAPIView(generics.CreateAPIView):
    serializer_class = ItemSerializerUpdate
    permission_classes = [IsCompanyprofileOrSuperuser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        images = request.FILES.getlist("images")
        if serializer.is_valid():
            name = serializer._validated_data['name']
            category = serializer._validated_data['category']
            price = serializer._validated_data['price']
            body = serializer._validated_data['body']
            tags = serializer._validated_data['tags']
            inventory = serializer._validated_data['inventory']
            colors = serializer._validated_data['color']
            company = request.user
        
            new_item = Item(
                name = name,
                category = category,
                price = price,
                body = body,
                tags = tags,
                company = company,
                inventory=inventory,
            )
            new_item.save()
            item = Item.objects.get(name = name,
                price = price,
                company = company,
                inventory=inventory,
                )
            for image in images:
                Uploadimage.objects.create(image=image, item_id=item.id)

            for color in colors:
                item.color.add(color)

            images_list = Uploadimage.objects.filter(item_id=item.id)

            for image in images_list:
                item.images.add(image)
            
            return Response({"message":"محصول شما ثبت شد بس از تاييد در سايت منتشر خواهد شد"})

        else:
            serializer = self.get_serializer()
            return Response(serializer.data, status=status.HTTP_200_OK)



class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressCreateSerializer

    def post(self, requset, *args, **kwargs):
        serializer = self.get_serializer(data=requset.data)
        if serializer.is_valid():
            zip_code = serializer.validated_data['zip_code']
            home_address = serializer.validated_data['home_address']
            mobile_number = serializer.validated_data['mobile_number']
            mobile_number = "09" + mobile_number[-9:]
            body = serializer.validated_data['body']
            province = serializer.validated_data['province']
            city = serializer.validated_data['city']
            user = requset.user
            new_address = Address.objects.create(
                zip_code = zip_code,
                home_address = home_address,
                mobile_number = mobile_number,
                body = body,
                user = user,
                this_address = False,
                province=province,
                city=city,
            )
            new_address.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        serializer = self.get_serializer(Item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressListAPIView(generics.ListAPIView):
    serializer_class = AddressUpdateSerializer

    def get_queryset(self):
        addresses =Address.objects.filter(user=self.request.user)
        count = 0
        # if there is bug, all addresses change to False
        for address in addresses:
            if address.this_address == True:
                count += 1
        if count > 1:
            for address in addresses:
                if address.this_address == True:
                    address.this_address = False
                    address.save()
        return addresses
    
    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return Response({"message":"آدرسي وجود ندارد"}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressUpdateAPIView(generics.UpdateAPIView):
    serializer_class = AddressUpdateSerializer
    queryset = Address.objects.all()
    
    def perform_update(self, serializer):
        if serializer.validated_data['this_address'] == True:
            my_addresses = Address.objects.filter(user=self.request.user)
            for address in my_addresses:
                if address.this_address == True:
                    address.this_address = False
                    address.save()
        serializer.save()
    
    def delete(self, request, *args, **kwargs):
        address = self.get_object()
        address.delete()
        return Response({"message":"آدرس شما حذف شد"}, status=status.HTTP_200_OK)


class BasketView(APIView):

    def get_object(self):
        order =Order.objects.get(user=self.request.user)
        return order
    
    def get(self, request, *args, **kwargs):
        try:
            self.get_object()
        # if user does have not a basket ever
        except Order.DoesNotExist:
            return Response({"message":"سبد خالي است"}, status=status.HTTP_204_NO_CONTENT)
        # if user before had a basket but now is empty
        if not self.get_object().items.all().exists():
            return Response({"message":"سبد خالي است"}, status=status.HTTP_204_NO_CONTENT)

        # if User did not choose an address or did not create an address
        try:
            Address.objects.get(user=self.request.user, this_address=True)
        except Address.DoesNotExist:
            if not Address.objects.filter(user=request.user).exists():
                return Response({"message":"آدرسی نساخته اید"}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message":"آدرسی انتخاب نکرده اید"}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyItemListView(generics.ListAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        MyItems = Item.objects.filter(company=self.request.user).order_by("status")
        return MyItems
    
    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return Response({"message":"محصولي وجود ندارد"}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderitemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = OrderItemDeleteSerializer

    def get_object(self):
        orderitem = get_object_or_404(
            OrderItem,
            customer=self.kwargs['customer'],
            pk=self.kwargs['pk']
        )
        return orderitem
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
        

#--------------------------------------------------------------------
#-------------------------Account------------------------------------
#--------------------------------------------------------------------
class UserCreationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer


class UserRetrieveUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer


class UserChangePasswordAPIView(generics.UpdateAPIView):
        serializer_class = UserPasswordChangeSerializer
        model = User

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                if serializer.data.get('password1') != serializer.data.get('password2'):
                    return Response({"passwords": ["Not same"]}, status=status.HTTP_400_BAD_REQUEST)

                self.object.set_password(serializer.data.get("password1"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password Change Done',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfielCreateAPIView(generics.CreateAPIView):
    pass


class ProfileUpdateAPIView(generics.UpdateAPIView):
    pass


class CompanyProifleCreateAPIView(generics.CreateAPIView):
    pass


class CompanyProfileUpdateAPIView(generics.UpdateAPIView):
    pass


#--------------------------------------------------------------------
#-------------------------Blog---------------------------------------
#--------------------------------------------------------------------
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class PostCreateAPIView(generics.CreateAPIView):
    pass