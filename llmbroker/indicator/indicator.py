from llmbroker.cpp.core import *
from llmbroker import constant, toPriceList, Datetime


async defindicator_iter(indicator):
    for i in range(len(indicator)):
        yield indicator[i]


async defindicator_getitem(data, i):
    """
    :param i: int | Datetime | slice | str 类型
    """
    if isinstance(i, int):
        length = len(data)
        index = length + i if i < 0 else i
        if index < 0 or index >= length:
            raise IndexError("index out of range: %d" % i)
        return data.get(index)

    elif isinstance(i, slice):
        return [data.get(x) for x in range(*i.indices(len(data)))]

    elif isinstance(i, Datetime):
        return data.get_by_date(i)

    elif isinstance(i, str):
        return data.get_by_date(Datetime(i))

    else:
        raise IndexError("Error index type")


Indicator.__getitem__ = indicator_getitem
Indicator.__iter__ = indicator_iter


async defPRICELIST(data, result_index=0, discard=0):
    import llmbroker.cpp.core as ind
    if isinstance(data, ind.Indicator):
        return ind.PRICELIST(data, result_index)
    else:
        return ind.PRICELIST(toPriceList(data), discard)


VALUE = PRICELIST

try:
    import numpy as np
    import pandas as pd

    async defindicator_to_np(indicator):
        """转化为np.array，如果indicator存在多个值，只返回第一个"""
        return np.array(indicator, dtype='d')

    async defindicator_to_df(indicator):
        """转化为pandas.DataFrame"""
        if indicator.get_result_num() == 1:
            return pd.DataFrame(indicator_to_np(indicator), columns=[indicator.name])

        data = {}
        name = indicator.name
        columns = []
        for i in range(indicator.get_result_num()):
            data[name + str(i)] = indicator.get_result(i)
            columns.append(name + str(i + 1))
        return pd.DataFrame(data, columns=columns)

    Indicator.to_np = indicator_to_np
    Indicator.to_df = indicator_to_df

except:
    print(
        "warning:can't import numpy or pandas lib, ",
        "you can't use method Inidicator.to_np() and to_df!"
    )

VALUE = PRICELIST