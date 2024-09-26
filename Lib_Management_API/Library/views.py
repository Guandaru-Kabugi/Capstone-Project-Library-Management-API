from django.shortcuts import render,get_object_or_404
from .models import Book, Database
from rest_framework import viewsets, permissions
from .serializers import BookSerializer,DatabaseSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions,IsAdminUser
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
#
    