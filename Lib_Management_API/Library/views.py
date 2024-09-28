from django.shortcuts import render,get_object_or_404
from .models import Book, Database
from rest_framework import viewsets, permissions
from .serializers import BookSerializer,DatabaseSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions,IsAdminUser
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import BookFilter
# Create your views here.
#there are different ways to implement permissions, either using djangpermissions or custombasepermissions
#we create a custom readonly permission
#HERE, I WANT TO ENSURE THAT ONLY THOSE WITH ADMIN PRIVILEGES CAN MAKE THESE CHANGES
class BookPermission(permissions.BasePermission):
    #This has permission is good with creating of a new object
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.has_perm('Library.create')
        return True
    #recommended when making changes to existing objects. \
        # django permissions documentations provide actions to be used \
            # it enables the developer to assign specific roles
    def has_object_permission(self, request, view, obj):
        if view.action in ['update','partial_update']:
            return request.user.has_perm('Library.edit')
        elif view.action == 'destroy':
            return request.user.has_perm('Library.delete')
        return True

#we create the viewset for database creation.\
    # This is sensitive because when you delete a database you delete a book. \
        # Therefore, only the superuser can create those databases or delete them,\
            # the admin can only perform crud operations on books
class ObjectReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser #we want only superusers to have the rest of the permissions for crud operations
    
#Next, we create the databaseviewset
class DatabaseView(viewsets.ModelViewSet):
    """
    {
        "database_name":"samplename"
    }
    This is a post method that expects this input. Only superusers have access
    """
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes=[ObjectReadOnlyPermission]
#Next, we create the Bookviewset
@permission_classes([IsAuthenticated,BookPermission])
class BookView(viewsets.ModelViewSet):
    """
    post method. Only admins can add, edit, or delete books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend] #It is a good filter approach that allows the use of different filter approaches
    filterset_class = BookFilter #I pass the bookfilter so that I can now search with greater than
#
@permission_classes([IsAuthenticated])
class BookList(ListAPIView):
    """
    This is a get method
    It lists the number of books present and their details
    You can filter by title and number_of_copies
    You can also filter using number_of_copies__gt=int to check books with copies above
    a specific integer.
    """
    serializer_class = BookSerializer #I have to serialize the results
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend] #It is a good filter approach that allows the use of different filter approaches
    filterset_fields = ['title','isbn','author','number_of_copies'] #this is a supplement that allows users to also get results based on specific number of copies present
    filterset_class = BookFilter #I pass the bookfilter so that I can now search with greater than
    
        
    
    
    