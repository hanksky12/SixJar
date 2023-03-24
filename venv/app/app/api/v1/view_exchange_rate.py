from flask import Response
import json
import time
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc

from ... import celery, redis
from .schema import ExchangeRateResponseSchema, ExchangeRateSchema
from ...utils import ResponseTool, DecoratorTool, JwtTool, SchemaTool, CustomizeError


class ExchangeRateApi(MethodResource):
    @DecoratorTool.integrate(
        tags_list=["ExchangeRate"],
        request_schema=ExchangeRateSchema,
        response_schema=ExchangeRateResponseSchema,
        method="GET")
    def get(self, *args, **kwargs):
        target_currency = kwargs["target_currency"]
        base_currency = kwargs["base_currency"]
        rate_data = redis.hgetall('rate_data')
        try:
            target_rate = rate_data[f"{target_currency}"]
            base_rate = rate_data[f"{base_currency}"]
            rate = round(float(target_rate) / float(base_rate), 4)
            return ResponseTool.success(message="查詢成功", data={"rate": rate})
        except KeyError:
            return ResponseTool.success(message="查詢失敗，沒有此幣別")
        else:
            return ResponseTool.success(message="查詢失敗，沒有資料")
