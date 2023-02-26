from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MyPagination(PageNumberPagination):
    page_size = 10  # 每页返回多少条数据
    page_query_param = 'page_num'  # 指定查询第几页（页码），默认 page
    page_size_query_param = 'page_size'  # 定义每页显示多少条
    max_page_size = 50  # 每页最多显示多少条

    def get_paginated_response(self, data):
        """
        针对所有分页get方法重写
        :param data:
        :return:
        """
        code = 200
        msg = "成功"
        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.page.paginator.count),
            ('data', data)
        ]))
