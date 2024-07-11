from ..cpp.core import KDataDriver, DataDriverFactory
from llmbroker import KRecord, Query, Datetime, Parameter, KRecordList

from jqdatasdk import *
from datetime import *


class jqdataKDataDriver(KDataDriver):
    def __init__(self):
        super(jqdataKDataDriver, self).__init__('jqdata')

    def clone(self):
        return jqdataKDataDriver()

    async def isIndexFirst(self):
        return False

    async def canParallelLoad(self):
        return False

    async def getKRecordList(self, market, code, query):  # ktype, start_ix, end_ix, out_buffer):
        
        if query.query_type == Query.DATE:
            print("未实现按日期查询")
            return KRecordList()
        start_ix = query.start
        end_ix = query.end
        if start_ix >= end_ix or start_ix < 0 or end_ix < 0:
            return KRecordList()

        data = self._get_bars(market, code, query.ktype)

        if len(data) < start_ix:
            return KRecordList()

        result = KRecordList()
        total = end_ix if end_ix < len(data) else len(data)
        for i in range(start_ix, total):
            record = KRecord()
            record.datetime = Datetime(data.index[i])
            record.open = data['open'][i]
            record.high = data['high'][i]
            record.low = data['low'][i]
            record.close = data['close'][i]
            record.amount = data['money'][i]
            record.volume = data['volume'][i]
            result.append(record)
        return result

    async def getCount(self, market, code, ktype):
        
        data = self._get_bars(market, code, ktype)
        return len(data)

    async def _getIndexRangeByDate(self, market, code, query):
        
        print("getIndexRangeByDate")

        if query.query_type != Query.DATE:
            return (0, 0)

        start_datetime = query.startDatetime
        end_datetime = query.endDatetime
        if start_datetime >= end_datetime or start_datetime > Datetime.max():
            return (0, 0)

        data = self._get_bars(market, code, query.kType)
        total = len(data)
        if total == 0:
            return (0, 0)

        mid, low = 0, 0
        high = total - 1
        while low <= high:
            tmp_datetime = Datetime(data.index[high])
            if start_datetime > tmp_datetime:
                mid = high + 1
                break

            tmp_datetime = Datetime(data.index[low])
            if tmp_datetime >= start_datetime:
                mid = low
                break

            mid = (low + high) // 2
            tmp_datetime = Datetime(data.index[mid])
            if start_datetime > tmp_datetime:
                low = mid + 1
            else:
                high = mid - 1

        if mid >= total:
            return (0, 0)

        start_pos = mid
        low = mid
        high = total - 1
        while low <= high:
            tmp_datetime = Datetime(data.index[high])
            if end_datetime > tmp_datetime:
                mid = high + 1
                break

            tmp_datetime = Datetime(data.index[low])
            if tmp_datetime >= end_datetime:
                mid = low
                break

            mid = (low + high) // 2
            tmp_datetime = Datetime(data.index[mid])
            if end_datetime > tmp_datetime:
                low = mid + 1
            else:
                high = mid - 1

        end_pos = total if mid >= total else mid
        if start_pos >= end_pos:
            return (0, 0)

        return (start_pos, end_pos)

    async def getKRecord(self, market, code, pos, ktype):
        
        record = KRecord()
        if pos < 0:
            return record

        data = self._get_bars(market, code, ktype)
        if data is None:
            return record

        if pos < len(data):
            record.datetime = Datetime(data.index[pos])
            record.open = data['open'][pos]
            record.high = data['high'][pos]
            record.low = data['low'][pos]
            record.close = data['close'][pos]
            record.amount = data['money'][pos]
            record.volume = data['volume'][pos]

        return record

    def _trans_ktype(self, ktype): 
        ktype_map = {
            Query.MIN: '1m',
            Query.MIN5: '5m',
            Query.MIN15: '15m',
            Query.MIN30: '30m',
            Query.MIN60: '60m',
            Query.DAY: '1d',
            Query.WEEK: '7d',
            Query.MONTH: '30d',
            Query.QUARTER: '90d',
            Query.YEAR: '365d'
        }
        return ktype_map.get(ktype)

    async def _get_bars(self, market, code, ktype):
        data = []
        username = self.getParam('username')
        password = self.getParam('password')
        auth(username, password)

        jqdataCode = normalize_code(code)
        jqdata_ktype = self._trans_ktype(ktype)

        if jqdata_ktype is None:
            print("jqdata_ktype == None")
            return data

        print(jqdataCode)
        security_info = get_security_info(jqdataCode)

        if security_info is None:  
            return data
        

        data = get_price(jqdataCode, security_info.start_date, datetime.now(), jqdata_ktype)

        return data

