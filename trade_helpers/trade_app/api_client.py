# -*- coding: utf-8 -*-
from openapi_client import openapi
from openapi_client.openapi_streaming import print_event, run_stream_consumer
from openapi_genclient.models.market_instrument import MarketInstrument
from openapi_genclient.models.candle import Candle
from typing import List
from enum import Enum
import json


class EOrderType(Enum):
    BUY = "Buy"
    SELL = "Sell"


class EInterval(Enum):
    MIN_ONE = "1min"
    MIN_TWO = "2min"
    MIN_THREE = "3min"
    MIN_FIVE = "5min"
    MIN_TEN = "10min"
    MIN_FIFTEEN = "15min"
    MIN_THIRTY = "30min"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class ApiClient:
    def __init__(self, token):
        self.__token = token
        self.__cli_impl = openapi.sandbox_api_client(self.__token)
        self.__cli_impl.sandbox.sandbox_register_post()
        self.__cli_impl.sandbox.sandbox_clear_post()
        self.__cli_impl.sandbox.sandbox_currencies_balance_post(
            sandbox_set_currency_balance_request={"currency": "USD", "balance": 1000}
        )

    def set_balance(self, usd_value):
        balance_set = self.__cli_impl.sandbox.sandbox_currencies_balance_post({"currency": "USD", "balance": usd_value})
        print("balance")
        print(balance_set)
        print()

    def print_orders(self):
        orders = self.__cli_impl.orders.orders_get()
        print("active orders")
        print(orders)
        print()

    def make_order(self, a_figi, a_count, a_price, a_type: EOrderType):
        order_response = self.__cli_impl.orders.orders_limit_order_post(
            figi=a_figi,
            limit_order_request={"lots": a_count, "operation": a_type.value, "price": a_price}
        )
        print("make order")
        print(order_response)
        print()
        return order_response

    def cancel_order(self, a_order_id):  # won't work in sandbox - orders are being instantly executed
        cancellation_result = self.__cli_impl.orders.orders_cancel_post(order_id=a_order_id)
        print("cancel order")
        print(cancellation_result)
        print()

    def get_stocks(self) -> List[MarketInstrument]:
        response = self.__cli_impl.market.market_stocks_get()
        return response.payload.instruments

    def get_candles(self, figi: str, start, end, interval: EInterval) -> List[Candle]:
        response = self.__cli_impl.market.market_candles_get(figi, start, end, interval.value)
        return response.payload.candles

    def run_candle_subscription(self, figis: List[str], interval: EInterval):
        candles_to_subscribe = []
        for f in figis:
            candles_to_subscribe.append({'figi': f, 'interval': interval.value})
        run_stream_consumer(self.__token,
                            candles_to_subscribe, [], [],
                            on_candle_event=print_event,
                            on_orderbook_event=print_event,
                            on_instrument_info_event=print_event)
