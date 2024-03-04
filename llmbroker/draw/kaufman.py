from llmbroker import (
    Query, StockManager, AMA, STDEV, CVAL, PRICELIST, EMA, CLOSE, HIGH, LOW, OPEN, KDATA, POS,
    SG_Single, SG_Cross, SG_Flex, BUSINESS
)
from .drawplot import (
    show_gcf, create_figure, ax_set_locator_formatter, adjust_axes_show, ax_draw_macd
)


def draw(
    stock,
    query=Query(-130),
    n=10,
    filter_n=20,
    filter_p=0.1,
    sg_type="CROSS",
    show_high_low=False,
    arrow_style=1
):
    """绘制佩里.J.考夫曼（Perry J.Kaufman） 自适应移动平均系统(AMA)"""
    kdata = stock.get_kdata(query)

    ax1, ax2 = create_figure(2)
    kdata.plot(axes=ax1)

    cama = AMA(CLOSE(kdata), n=n)
    cama.name = "CAMA"
    cama.plot(axes=ax1, color='b', legend_on=True, kref=kdata)

    hama = AMA(HIGH(kdata), n=n)
    hama.name = "HAMA"
    hstd = STDEV(hama, n)
    lama = AMA(LOW(kdata), n=n)
    lama.name = "LAMA"
    lstd = STDEV(lama, n)
    fy1 = list(lama - lstd)[lstd.discard:]
    fy2 = list(hama + hstd)[hstd.discard:]
    ax1.fill_between(range(lstd.discard, len(kdata)), fy1, fy2, alpha=0.2, color='y')

    if show_high_low:
        hama.plot(axes=ax1, color='r', legend_on=True, kref=kdata)
        lama.plot(axes=ax1, color='g', legend_on=True, kref=kdata)

    if sg_type == 'CROSS':
        fast_op = AMA(n=n)
        slow_op = EMA(n=2 * n)(fast_op)
        sg = SG_Cross(fast_op, slow_op)
        sg.plot(axes=ax1, kdata=kdata)
        ind = slow_op(KDATA(kdata))
        ind.name = "EMA(CAMA)"
        ind.plot(axes=ax1, color='m', legend_on=True, kref=kdata)

    elif sg_type == 'SINGLE':
        sg = SG_Single(cama, filter_n=filter_n, filter_p=filter_p)
        sg.plot(axes=ax1, kdata=kdata)

    else:
        print("sg_type only in ('CORSS', 'SINGLE')")

    cer = PRICELIST(cama, 1)
    label = "ER(%s)" % cer[-1]
    cer.plot(axes=ax2, color='b', marker='o', label=label, legend_on=False, text_on=True, kref=kdata)

    c = CLOSE(kdata)
    CVAL(c, 0.8).plot(axes=ax2, color='r', linestyle='--', kref=kdata)
    CVAL(c, -0.6).plot(axes=ax2, color='r', linestyle='--', kref=kdata)
    CVAL(c, -0.8).plot(axes=ax2, color='r', linestyle='--', kref=kdata)
    CVAL(c, 0).plot(axes=ax2, color='k', linestyle='-', kref=kdata)
    
    
    
    

    ax1.set_xlim((0, len(kdata)))
    ax_set_locator_formatter(ax1, kdata.get_datetime_list(), query.ktype)
    adjust_axes_show([ax1, ax2])
    return show_gcf()


def draw2(
    block,
    query=Query(-130),
    ama1=AMA(n=10, fast_n=2, slow_n=30),
    ama2=None,
    n=10,
    filter_n=20,
    filter_p=0.1,
    sg_type='CROSS',
    show_high_low=True,
    arrow_style=1
):
    """绘制佩里.J.考夫曼（Perry J.Kaufman） 自适应移动平均系统(AMA)"""
    sm = StockManager.instance()
    if block.name == 'SZ':
        kdata = sm['sz000001'].get_kdata(query)
    elif block.name == 'GEM':
        kdata = sm['sz399006'].get_kdata(query)
    else:
        kdata = sm['sh000001'].get_kdata(query)

    ax1, ax2, ax3 = create_figure(3)
    kdata.plot(axes=ax1)

    cama = AMA(CLOSE(kdata), n=n)
    cama.name = "CAMA"
    cama.plot(axes=ax1, color='b', legend_on=True, kref=kdata)

    hama = AMA(HIGH(kdata), n=n)
    hama.name = "HAMA"
    hstd = STDEV(hama, n)
    lama = AMA(LOW(kdata), n=n)
    lama.name = "LAMA"
    lstd = STDEV(lama, n)
    fy1 = list(lama - lstd)[lstd.discard:]
    fy2 = list(hama + hstd)[hstd.discard:]
    ax1.fill_between(range(lstd.discard, len(kdata)), fy1, fy2, alpha=0.2, color='y')

    if show_high_low:
        hama.plot(axes=ax1, color='r', legend_on=True, kref=kdata)
        lama.plot(axes=ax1, color='g', legend_on=True, kref=kdata)

    if sg_type == 'CROSS':
        fast_op = AMA(n=n)
        slow_op = EMA(n=2 * n)(fast_op)
        sg = SG_Cross(fast_op, slow_op)
        sg.plot(axes=ax1, kdata=kdata)
        ind = slow_op(KDATA(kdata))
        ind.name = "EMA(CAMA)"
        ind.plot(axes=ax1, color='m', legend_on=True, kref=kdata)

    elif sg_type == 'SINGLE':
        sg = SG_Single(cama, filter_n=filter_n, filter_p=filter_p)
        sg.plot(axes=ax1, kdata=kdata)

    else:
        print("sg_type only in ('CORSS', 'SINGLE')")

    a = POS(block, query, SG_Flex(AMA(n=3), 6))
    a.name = "POS(3)"
    a.plot(axes=ax2, color='b', marker='.', legend_on=True, kref=kdata)
    a = POS(block, query, SG_Flex(AMA(n=30), 60))
    a.name = "POS(30)"
    a.plot(axes=ax2, color='g', marker='.', legend_on=True, kref=kdata)

    c = CLOSE(kdata)
    CVAL(c, 0.8).plot(axes=ax2, color='r', linestyle='--', kref=kdata)
    CVAL(c, 0.2).plot(axes=ax2, color='r', linestyle='--', kref=kdata)

    if ama1.name == "AMA":
        cer = PRICELIST(cama, 1)
        label = "ER(%s)" % cer[-1]
        cer.plot(axes=ax3, color='b', marker='.', label=label, legend_on=False, text_on=True, kref=kdata)
        CVAL(c, 0.8).plot(axes=ax3, color='r', linestyle='--', kref=kdata)
        CVAL(c, -0.6).plot(axes=ax3, color='r', linestyle='--', kref=kdata)
        CVAL(c, -0.8).plot(axes=ax3, color='r', linestyle='--', kref=kdata)
        CVAL(c, 0).plot(axes=ax3, color='k', linestyle='-', kref=kdata)
    else:
        ax_draw_macd(ax2, kdata)
    

    ax1.set_xlim((0, len(kdata)))
    ax_set_locator_formatter(ax1, kdata.get_datetime_list(), query.ktype)
    adjust_axes_show([ax1, ax2])
    return show_gcf()
