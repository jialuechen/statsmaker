from .indicator import *


def KDJ(kdata=None, n=9, m1=3, m2=3):

    rsv = (CLOSE() - LLV(LOW(), n)) / (HHV(HIGH(), n) - LLV(LOW(), n)) * 100
    k = SMA(rsv, m1, 1)
    d = SMA(k, m2, 1)
    j = 3 * k - 2 * d
    if kdata is not None:
        k.set_context(kdata)
        j.set_context(kdata)
        d.set_context(kdata)
    return k, d, j


def RSI(kdata=None, N1=6, N2=12, N3=24):
    
    LC = REF(CLOSE(), 1)
    rsi1 = SMA(MAX(CLOSE() - LC, 0), N1, 1) / SMA(ABS(CLOSE() - LC), N1, 1) * 100
    rsi2 = SMA(MAX(CLOSE() - LC, 0), N2, 1) / SMA(ABS(CLOSE() - LC), N2, 1) * 100
    rsi3 = SMA(MAX(CLOSE() - LC, 0), N3, 1) / SMA(ABS(CLOSE() - LC), N3, 1) * 100

    if kdata is not None:
        rsi1.set_context(kdata)
        rsi2.set_context(kdata)
        rsi3.set_context(kdata)
    return rsi1, rsi2, rsi3
