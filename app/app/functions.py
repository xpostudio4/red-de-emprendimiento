"""
The purpose of this function files is to keep all the helpfull
functions constanlly used in a django base project.
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginated_list(request, object_class, list_length, order=None, *args, **kwargs):
    """
    The purpose of this function is to generate the list of all the
    paginated elements to be displayed on the diferent pages.
    keyword arguments:
    object_class -- The object we'll be calling as a list
    order -- should it be ordered by any variable
    list_length -- How many elements we'll display on a single page
    *args, **kwargs -- The filters when calling the objects.
    """
    object_list = object_class.objects.filter(*args, **kwargs)
    if order is not None:
        object_list.order_by(order)
    paginator = Paginator(object_list, list_length) #show 20 c per page
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        #if the page is not an integer, deliver the first page.
        objects = paginator.page(1)
    except EmptyPage:
        #if page is out range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return objects
