# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Crawl.py
# Author  : Arif Dzikrullah
# E-Mail  : ardzix@hotmail.com
#
# Please write your identity if you change this file
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from django.db.models import  Q
import types
import datetime
import arrow
from django.conf import settings
from json_response import JSONResponse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# =============================================
# The Datatable
# this class serve datatable client request
# so the client can request data, sort, search and paginate
#
# i know this file is a mess, i hope you can improve this
# =============================================
class Datatable(object):

    # Initialize class attribute
    request = None
    obj = None
    defer = []
    key = ""
    deff_button = True
    custom_button = []
    time_format = "MMM. D, YYYY h:mm a"
    offset = 0
    limit = 10
    data = {}
    ordering = ""
    posts = None
    error = False
    error_messages = None

    # When you instantiate a variable with this class, you need to provide:
    # - request   : the request needed to get url parameter sent by client
    # - obj       : this is model object
    # - defer     : list of column that need to be returned
    # - key       : column name for table id
    # - deff_button : if true, button edit and delete will be shown on last column automatically
    # - custom_button : custom button that will be rendered after default button

    def __init__(self, request, obj, defer, key="id62", deff_button=True,custom_button=[]):
        self.request = request
        self.obj = obj
        self.defer = defer
        self.key = key
        self.deff_button = deff_button
        self.custom_button = custom_button
        self.offset = int(request.GET.get("start",0))
        self.limit = int(request.GET.get("length",10)) + self.offset

        # Get ordering parameter
        if not request.GET.get("order[0][dir]","") == "asc":
            self.ordering = "-"
            
        # Get search/filter value
        filter_qry = request.GET.get('search[value]','')
        
        # If search/filter value not provided
        if filter_qry == '':
            # We don't perform search
            self.posts = obj
            self.data['recordsFiltered'] = obj.count()
        else:
            # else, we perform search
            search = self.search(filter_qry=filter_qry)
            # If search returned none
            if search != None:
                # Than it was error, so we need to perform search error
                self.search_error(error_messages=search)

        # Then we perform ordering
        self.order()

        # Put some data parameter
        self.data['draw'] = request.GET.get('draw')
        self.data['recordsTotal'] = obj.count()

        # Perform append
        self.append()


    # get data is called when you need data in this instance
    def get_data(self):
        # if there is an error in this instance
        if self.error:
            # then we return the error message
            return self.error_messages

        # Finally we return the data on this instace
        return JSONResponse(self.data)

    # Set error status true and give error message if there is no search result 
    def search_error(self,error_messages):
        self.error = True
        self.error_messages = error_messages

    # We make filter query from search value in this method
    def search(self,filter_qry):
        search_defer = []
        # for every defer in this instance
        for n in range(len(self.defer)):
            # we check, is it searchable or not? searchable parameter sent by client in request url
            if self.request.GET.get('columns['+str(n)+'][searchable]','false') == 'true':
                # if it is searchable, we append it to search defer list
                search_defer.append(self.defer[n]+"__icontains")

        # We make filter queries from the defer
        queries = [Q(**{f: filter_qry}) for f in search_defer]

        # We instantiate a variable called QS from Q class
        qs = Q()
        # for every query in filter queries
        for query in queries:
            # we make or query for every search defer with same value
            qs = qs | query

        # Then we try to 
        try:
            # append the filter methode to the queryset object with qs object as parameter
            self.posts = self.obj.filter(qs)
            # also the record filtered rows count need to passed to the return
            self.data['recordsFiltered'] = self.obj.filter(qs).count()
        # if we failed to try
        except Exception as e:
            # we sent an error response to client
            return JSONResponse({'error' : 'error in search parameter', 'error detail': str(e), 'suggestion' : 'Only enable varchar data type only for search'})

    # we add ordering method to queryset object with ordering parameter sent by client
    def order(self):
        self.posts = self.posts.order_by(self.ordering+self.defer[int(self.request.GET.get('order[0][column]',0))])

    # this method appending every field from result of post object to datatable row list
    def append(self): 
        self.data['data'] = []
        n = 0
        # for every post result in page requested by client, we do:
        for v in self.posts[self.offset:self.limit]:
            d_list = []
            # loop for every defer then
            for x in self.defer:
                # get attribute of post result with defer as a key
                attr = getattr(v, x)
                # if the attribute is a method
                if type(attr) == types.MethodType:
                    # we convert the attribute velue then append it to result row
                    d_list.append(str(attr()))
                # if the attribute is datetime
                elif str(type(attr)) == "<type 'datetime.datetime'>":
                    # we convert its value (datetime) to local timezone and append it
                    locale_time = arrow.get(attr).to(settings.TIME_ZONE)
                    d_list.append(locale_time.format(self.time_format))
                # else
                else:
                    # we convert its attribute directly to a string and append it
                    d_list.append(str(attr))

            button = ""

            # if deff button is True
            if self.deff_button:
                # we add the rendered deffault button
                button = button+'<button type="button" style="margin:2px" class="btn btn-sm btn-primary btn-cons btn-animated from-left pg pg-arrow_right" onclick="edit_data(\''+str(getattr(v, self.key))+'\')"><span><i class="fa fa-edit"></i>&nbsp;Detail &amp; Edit</span></button><button type="button" style="margin:2px" class="btn btn-sm btn-danger btn-cons btn-animated from-left pg pg-arrow_right" onclick="delete_data(\''+str(getattr(v, self.key))+'\')"><span><i class="fa fa-trash"></i>&nbsp;Delete</span></button>'

            # for every custom button provided in parameter:
            for b in self.custom_button:
                # we render the button html
                button = button+'<button type="button" style="'+b['style']+'" class="'+b['class']+'" onclick="'+b['on_click']+'(\''+str(getattr(v, self.key))+'\')"><span><i class="fa '+b['icon']+'"></i>&nbsp;'+b['text']+'</span></button>'
            # Then we append the rendered button to the field
            d_list.append(button)
            self.data['data'].append(tuple(d_list))
            n = n+1