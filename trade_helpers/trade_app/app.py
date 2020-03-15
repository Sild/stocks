# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget

from trade_helpers.trade_app.config import Config
from trade_helpers.trade_app.api_client import ApiClient, EInterval

from trade_helpers.trade_app.gui import TradeAppWindow
from datetime import datetime, timedelta
import pytz


class TradeApp:
    def __init__(self):
        self.__config = Config()
        self.__api_client = ApiClient(self.__config.api_token)

    def __collect_candle_stat(self, figi, start, end, interval):
        candles = self.__api_client.get_candles(figi, start, end, EInterval.MIN_FIFTEEN)
        volume = 0
        low_min = 99999999999.9
        high_max = -1.0
        if len(candles) == 0:
            return 0, 0
        for c in candles:
            volume += c.v
            low_min = min(low_min, c.l)
            high_max = max(high_max, c.h)
        close = candles[-1].c
        dec_percent = (close - low_min) / close
        inc_percent = (high_max - close) / close
        return volume, min(inc_percent, dec_percent)

    def __get_promising_stocks(self):
        # средний объем торгов в следующие  топ 10% среди всех
        # диапазон изменения - больше 6% (+-3%)за этот интервал
        # (-2, +4) часа за предыдущий день
        # (-2, 0) сегодня
        # средний объем торгов сегодня за предыдущий
        stocks = self.__api_client.get_stocks()

        self.__api_client.run_candle_subsciribtion([s.figi for s in stocks], EInterval.MIN_ONE)

        today_end_ts = datetime.now(pytz.timezone("Europe/Moscow")) - timedelta(days=3)
        today_start_ts = today_end_ts - timedelta(hours=2)
        yesterday_end_ts = today_end_ts - timedelta(days=1) + timedelta(hours=4)
        yesterday_start_ts = today_end_ts - timedelta(days=1) - timedelta(hours=2)

        figi_today_volumes = dict()
        figi_today_dispersion = dict()

        figi_yesterday_volumes = dict()
        figi_yesterday_dispersion = dict()
        i = 0
        print(len(stocks))
        for s in stocks:
            i += 2
            if i > 10:
                break
            figi_today_volumes[s.figi], figi_today_dispersion[s.figi] = self.__collect_candle_stat(
                s.figi, today_start_ts, today_end_ts, EInterval.MIN_FIFTEEN
            )
            figi_yesterday_volumes[s.figi], figi_yesterday_dispersion[s.figi] = self.__collect_candle_stat(
                s.figi, yesterday_start_ts, yesterday_end_ts, EInterval.MIN_FIFTEEN
            )
        print(figi_today_volumes)
        print(figi_today_dispersion)
        filtered = filter(lambda s:
                          s.figi in figi_today_volumes.keys() and figi_today_volumes[s.figi] > 0 and figi_today_dispersion[s.figi] >= 0.03
                          and figi_yesterday_volumes[s.figi] > 0 and figi_yesterday_dispersion[s.figi] >= 0.03, stocks)
        filtered_sorted = sorted(filtered, key=lambda s: figi_today_volumes[s.figi], reverse=True)
        print(filtered_sorted)
        return []
        # return stocks

    def run(self):
        stocks = self.__get_promising_stocks()
        for s in stocks:
            print(s)
        return
        app = QApplication(sys.argv)

        window = TradeAppWindow()
        window.show()

        # Start the event loop.
        app.exec_()
        self.run_rest()
        self.__api_client.run_stream(self.__config.api_token)

    def run_rest(self):
        self.__api_client.set_balance(usd_value=1000)
        self.__api_client.print_orders()
        # order_response = self.__api_client.make_order()
        self.__api_client.print_orders()


