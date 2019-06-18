# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from rest_framework import generics
from rest_framework.response import Response


class ListByIdsView(generics.GenericAPIVie):

    def get(self, request):
        if 'id' in request.query_params:
            _id = request.query_params['id']
            return Response(self.get_item(self.model.objects.get(pk=_id)))
        elif 'ids' in request.query_params:
            return Response(self.get_list_items(self.get_queryset()))
        else:
            return self._i_get(request)

    def get_queryset(self):
        if self.queryset:
            return self.queryset.all()
        if 'ids' in self.request.query_params:
            if self.request.query_params['ids'] == '':
                raise LookupError(
                    'get "ids" in request.query_params with illegal value')

            #http://blog.mathieu-leplatre.info/django-create-a-queryset-from-a-list-preserving-order.html
            #按照ids的顺序返回一个queryset
            id_list = [int(pk) for pk in self.request.query_params['ids'].split(',')]
            ordering = 'FIELD(%s.id, %s)' % (self.model._meta.db_table,
                                             ','.join([str(pk) for pk in id_list]))
            queryset = self.model.objects.filter(pk__in=id_list).extra(
                select={'ordering': ordering}, order_by=('ordering',))