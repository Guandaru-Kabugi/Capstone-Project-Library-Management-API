import django_filters
from .models import Book
#here, I learned that we can implement a custom filter using django_filters.filterset
#I am filtering through numbers, which is why I have Numberfilter
class BookFilter(django_filters.FilterSet):
    #I add two underscores to tell django I am using number of copies to get greater than value
    #I then add field name and the lookup expression, in this case gt
    number_of_copies__gt = django_filters.NumberFilter(field_name='number_of_copies', lookup_expr='gt')
    #like in serializers, I get the model and also the fields which will be passed as filter_class
    title = django_filters.CharFilter(field_name='title', lookup_expr='iexact')  # Case-insensitive exact match
    isbn = django_filters.CharFilter(field_name='isbn',lookup_expr='iexact') #we want to ensure that the isbn contains these details
    published_date = django_filters.DateFilter(field_name='published_date',lookup_expr='icontains')
    number_of_copies = django_filters.NumberFilter(field_name='number_of_copies',lookup_expr='iexact')

    class Meta:
        model = Book
        fields = ['number_of_copies__gt', 'title','isbn','number_of_copies']
