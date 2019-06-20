# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from rest_framework import serializers as rf_serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class MyForeignKeyField(rf_serializers.RelatedField):
    """
    自定义外键的序列化和反序列化的方式
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(
                query_field1=self.parent.initial_data['query_field1'],
                query_field2=self.parent.initial_data['query_field2']
            )
        except ObjectDoesNotExist:
            raise ValidationError(
                'does_not_exist: query_field1: {}, query_field2: {}'.format(
                    self.parent.initial_data['query_field1'], self.parent.initial_data['query_field2']
                )
            )
        except (TypeError, ValueError):
            raise ValidationError('incorrect_type: {}'.format(type(data).__name__))

    def to_representation(self, value):
        """
        返回需要的属性，而不是主键或者field的字符串表示
        """
        return value.preferred_field
