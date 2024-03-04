import sys
import datetime
import numpy as np
import matplotlib
from pylab import Rectangle, gca, figure, ylabel, axes, draw
from matplotlib.lines import Line2D, TICKLEFT, TICKRIGHT
from matplotlib.ticker import FuncFormatter, FixedLocator

from llmbroker import *

from .common import get_draw_title


def create_one_axes_figure(figsize=(10, 6)):
    
    rect1 = [0.05, 0.05, 0.9, 0.90]
    fg = figure(figsize=figsize)
    ax1 = fg.add_axes(rect1)
    return ax1


def create_two_axes_figure(figsize=(10, 8)):
    
    rect1 = [0.05, 0.35, 0.9, 0.60]
    rect2 = [0.05, 0.05, 0.9, 0.30]

    fg = figure(figsize=figsize)
    ax1 = fg.add_axes(rect1)
    ax2 = fg.add_axes(rect2, sharex=ax1)

    return ax1, ax2


def create_three_axes_figure(figsize=(10, 8)):
    """生成一个含有3个坐标轴的figure，并返回坐标轴列表
    
    :param figsize: (宽, 高)
    :return: (ax1, ax2, ax3)
    """
    rect1 = [0.05, 0.45, 0.9, 0.50]
    rect2 = [0.05, 0.25, 0.9, 0.20]
    rect3 = [0.05, 0.05, 0.9, 0.20]

    fg = figure(figsize=figsize)
    ax1 = fg.add_axes(rect1)
    ax2 = fg.add_axes(rect2, sharex=ax1)
    ax3 = fg.add_axes(rect3, sharex=ax1)

    return ax1, ax2, ax3


def create_four_axes_figure(figsize=(10, 8)):
    
    rect1 = [0.05, 0.50, 0.9, 0.45]
    rect2 = [0.05, 0.35, 0.9, 0.15]
    rect3 = [0.05, 0.20, 0.9, 0.15]
    rect4 = [0.05, 0.05, 0.9, 0.15]

    fg = figure(figsize=figsize)
    ax1 = fg.add_axes(rect1)
    ax2 = fg.add_axes(rect2, sharex=ax1)
    ax3 = fg.add_axes(rect3, sharex=ax1)
    ax4 = fg.add_axes(rect4, sharex=ax1)

    return ax1, ax2, ax3, ax4


def create_figure(n=1, figsize=(10, 8)):
    
    if n == 1:
        return create_one_axes_figure(figsize)
    elif n == 2:
        return create_two_axes_figure(figsize)
    elif n == 3:
        return create_three_axes_figure(figsize)
    elif n == 4:
        return create_four_axes_figure(figsize)
    else:
        print("Max support axes number is 4!")
        return None


class StockFuncFormatter(object):

    def __init__(self, ix2date):
        self.__ix2date = ix2date

    def __call__(self, x, pos=None):  
        result = ''
        ix = int(x)
        if ix in self.__ix2date:
            result = self.__ix2date[ix]
        return result


def getDayLocatorAndFormatter(dates):
    """获取显示日线时使用的Major Locator和Major Formatter"""
    sep = len(dates) / 8
    loc = [
        (
            i, str(d) if
            (i !=
             (len(dates) - 1)) and (i % sep != 0) else "{}-{}-{}".format(d.year, d.month, d.day)
        ) for i, d in enumerate(dates)
    ]
    fixed_loc = [
        i for i in range(len(dates)) if (i == (len(dates) - 1)) or (i != 0 and i % sep == 0)
    ]

    month_loc = FixedLocator(fixed_loc)
    month_fm = FuncFormatter(StockFuncFormatter(dict(loc)))
    return month_loc, month_fm


def getMinLocatorAndFormatter(dates):
    sep = len(dates) / 5
    loc = [
        (
            i, str(d)
            if i % sep != 0 else "{}-{}-{} {}:{}".format(d.year, d.month, d.day, d.hour, d.minute)
        ) for i, d in enumerate(dates)
    ]
    fixed_loc = [i for i in range(len(dates)) if i != 0 and i % sep == 0]

    month_loc = FixedLocator(fixed_loc)
    month_fm = FuncFormatter(StockFuncFormatter(dict(loc)))
    return month_loc, month_fm


def adjust_axes_show(axeslist):
    for ax in axeslist[:-1]:
        for label in ax.get_xticklabels():
            label.set_visible(False)
        ylabels = ax.get_yticklabels()
        ylabels[0].set_visible(False)


def kplot(kdata, new=True, axes=None, colorup='r', colordown='g'):

    if not kdata:
        print("kdata is None")
        return

    if not axes:
        axes = create_figure() if new else gca()

    alpha = 1.0
    width = 0.6
    OFFSET = width / 2.0
    rfcolor = matplotlib.rcParams['axes.facecolor']
    for i in range(len(kdata)):
        record = kdata[i]
        open, high, low, close = record.open, record.high, record.low, record.close
        if close >= open:
            color = colorup
            lower = open
            height = close - open
            rect = Rectangle(
                xy=(i - OFFSET, lower),
                width=width,
                height=height,
                facecolor=rfcolor,
                edgecolor=color
            )
        else:
            color = colordown
            lower = close
            height = open - close
            rect = Rectangle(
                xy=(i - OFFSET, lower),
                width=width,
                height=height,
                facecolor=color,
                edgecolor=color
            )

        vline1 = Line2D(
            xdata=(i, i), ydata=(low, lower), color=color, linewidth=0.5, antialiased=True
        )
        vline2 = Line2D(
            xdata=(i, i),
            ydata=(lower + height, high),
            color=color,
            linewidth=0.5,
            antialiased=True
        )
        rect.set_alpha(alpha)

        axes.add_line(vline1)
        axes.add_line(vline2)
        axes.add_patch(rect)

    title = get_draw_title(kdata)
    axes.set_title(title)
    last_record = kdata[-1]
    color = 'r' if last_record.close > kdata[-2].close else 'g'
    text = u'%s 开:%.2f 高:%.2f 低:%.2f 收:%.2f 涨幅:%.2f%%' % (
        last_record.datetime.number / 10000, last_record.open, last_record.high, last_record.low,
        last_record.close, 100 * (last_record.close - kdata[-2].close) / kdata[-2].close
    )
    axes.text(
        0.99,
        0.97,
        text,
        horizontalalignment='right',
        verticalalignment='top',
        transform=axes.transAxes,
        color=color
    )

    axes.autoscale_view()
    axes.set_xlim(-1, len(kdata) + 1)
    ax_set_locator_formatter(axes, kdata.get_datetime_list(), kdata.get_query().ktype)
    


def mkplot(kdata, new=True, axes=None, colorup='r', colordown='g', ticksize=3):
    if not kdata:
        print("kdata is None")
        return

    if not axes:
        axes = create_figure() if new else gca()

    for t in range(len(kdata)):
        record = kdata[t]
        open, high, low, close = record.open, record.high, record.low, record.close
        color = colorup if close >= open else colordown

        vline = Line2D(xdata=(t, t), ydata=(low, high), color=color, antialiased=False)
        oline = Line2D(
            xdata=(t, t),
            ydata=(open, open),
            color=color,
            antialiased=False,
            marker=TICKLEFT,
            markersize=ticksize
        )
        cline = Line2D(
            xdata=(t, t),
            ydata=(close, close),
            color=color,
            antialiased=False,
            markersize=ticksize,
            marker=TICKRIGHT
        )

        axes.add_line(vline)
        axes.add_line(oline)
        axes.add_line(cline)

    title = get_draw_title(kdata)
    axes.set_title(title)
    last_record = kdata[-1]
    color = 'r' if last_record.close > kdata[-2].close else 'g'
    text = u'%s 开:%.2f 高:%.2f 低:%.2f 收:%.2f' % (
        last_record.datetime.number / 10000, last_record.open, last_record.high, last_record.low,
        last_record.close
    )
    axes.text(
        0.99,
        0.97,
        text,
        horizontalalignment='right',
        verticalalignment='top',
        transform=axes.transAxes,
        color=color
    )

    axes.autoscale_view()
    axes.set_xlim(-1, len(kdata) + 1)
    ax_set_locator_formatter(axes, kdata.get_datetime_list(), kdata.get_query().ktype)
    


def iplot(
    indicator,
    new=True,
    axes=None,
    kref=None,
    legend_on=False,
    text_on=False,
    text_color='k',
    zero_on=False,
    label=None,
    *args,
    **kwargs
):
    if not indicator:
        print("indicator is None")
        return

    if not axes:
        axes = create_figure() if new else gca()

    if not label:
        label = "%s %.2f" % (indicator.long_name, indicator[-1])

    py_indicatr = [None if x == constant.null_price else x for x in indicator]
    axes.plot(py_indicatr, '-', label=label, *args, **kwargs)

    if legend_on:
        leg = axes.legend(loc='upper left')
        leg.get_frame().set_alpha(0.5)

    if text_on:
        if not axes.texts:
            axes.text(
                0.01,
                0.97,
                label,
                horizontalalignment='left',
                verticalalignment='top',
                transform=axes.transAxes,
                color=text_color
            )
        else:
            temp_str = axes.texts[0].get_text() + '  ' + label
            axes.texts[0].set_text(temp_str)

    if zero_on:
        ylim = axes.get_ylim()
        if ylim[0] < 0 < ylim[1]:
            axes.hlines(0, 0, len(indicator))

    axes.autoscale_view()
    axes.set_xlim(-1, len(indicator) + 1)
    if kref:
        ax_set_locator_formatter(axes, kref.get_datetime_list(), kref.get_query().ktype)
    


def ibar(
    indicator,
    new=True,
    axes=None,
    kref=None,
    legend_on=False,
    text_on=False,
    text_color='k',
    label=None,
    width=0.4,
    color='r',
    edgecolor='r',
    zero_on=False,
    *args,
    **kwargs
):
    if not indicator:
        print("indicator is None")
        return

    if not axes:
        axes = create_figure() if new else gca()

    if not label:
        label = "%s %.2f" % (indicator.long_name, indicator[-1])

    py_indicatr = [None if x == constant.null_price else x for x in indicator]
    x = [i - 0.2 for i in range(len(indicator))]
    y = py_indicatr

    axes.bar(x, py_indicatr, width=width, color=color, edgecolor=edgecolor, *args, **kwargs)

    if legend_on:
        leg = axes.legend(loc='upper left')
        leg.get_frame().set_alpha(0.5)

    if text_on:
        if not axes.texts:
            axes.text(
                0.01,
                0.97,
                label,
                horizontalalignment='left',
                verticalalignment='top',
                transform=axes.transAxes,
                color=text_color
            )
        else:
            temp_str = axes.texts[0].get_text() + '  ' + label
            axes.texts[0].set_text(temp_str)

    if zero_on:
        ylim = axes.get_ylim()
        if ylim[0] < 0 < ylim[1]:
            axes.hlines(0, 0, len(indicator))

    axes.autoscale_view()
    axes.set_xlim(-1, len(indicator) + 1)
    if kref:
        ax_set_locator_formatter(axes, kref.get_datetime_list(), kref.get_query().ktype)
    


def ax_draw_macd(axes, kdata, n1=12, n2=26, n3=9):
    
    macd = MACD(CLOSE(kdata), n1, n2, n3)
    bmacd, fmacd, smacd = macd.get_result(0), macd.get_result(1), macd.get_result(2)

    text = 'MACD(%s,%s,%s) DIF:%.2f, DEA:%.2f, BAR:%.2f' % (
        n1, n2, n3, fmacd[-1], smacd[-1], bmacd[-1]
    )
    axes.text(
        0.01,
        0.97,
        text,
        horizontalalignment='left',
        verticalalignment='top',
        transform=axes.transAxes
    )
    total = len(kdata)
    x = [i - 0.2 for i in range(total)]
    x1 = [x[i] for i, d in enumerate(bmacd) if d > 0]
    y1 = [i for i in bmacd if i > 0]
    x2 = [x[i] for i, d in enumerate(bmacd) if d <= 0]
    y2 = [i for i in bmacd if i <= 0]
    axes.bar(x1, y1, width=0.4, color='r', edgecolor='r')
    axes.bar(x2, y2, width=0.4, color='g', edgecolor='g')

    axt = axes.twinx()
    axt.grid(False)
    axt.set_yticks([])
    fmacd.plot(axes=axt, linestyle='--', legend_on=False, text_on=False)
    smacd.plot(axes=axt, legend_on=False, text_on=False)

    for label in axt.get_xticklabels():
        label.set_visible(False)


def ax_draw_macd2(axes, ref, kdata, n1=12, n2=26, n3=9):
    macd = MACD(CLOSE(kdata), n1, n2, n3)
    bmacd, fmacd, smacd = macd.get_result(0), macd.get_result(1), macd.get_result(2)

    text = 'MACD(%s,%s,%s) DIF:%.2f, DEA:%.2f, BAR:%.2f' % (
        n1, n2, n3, fmacd[-1], smacd[-1], bmacd[-1]
    )
    axes.text(
        0.01,
        0.97,
        text,
        horizontalalignment='left',
        verticalalignment='top',
        transform=axes.transAxes
    )
    total = len(kdata)
    x = [i - 0.2 for i in range(0, total)]
    y = bmacd
    x1, x2, x3 = [x[0]], [], []
    y1, y2, y3 = [y[0]], [], []
    for i in range(1, total):
        if ref[i] - ref[i - 1] > 0 and y[i] - y[i - 1] > 0:
            x2.append(x[i])
            y2.append(y[i])
        elif ref[i] - ref[i - 1] < 0 and y[i] - y[i - 1] < 0:
            x3.append(x[i])
            y3.append(y[i])
        else:
            x1.append(x[i])
            y1.append(y[i])

    axes.bar(x1, y1, width=0.4, color='
    axes.bar(x2, y2, width=0.4, color='r', edgecolor='r')
    axes.bar(x3, y3, width=0.4, color='g', edgecolor='g')

    axt = axes.twinx()
    axt.grid(False)
    axt.set_yticks([])
    fmacd.plot(axes=axt, linestyle='--', legend_on=False, text_on=False)
    smacd.plot(axes=axt, legend_on=False, text_on=False)

    for label in axt.get_xticklabels():
        label.set_visible(False)


def sgplot(sg, new=True, axes=None, style=1, kdata=None):
    
    kdata = sg.to if kdata is None else kdata
    refdates = kdata.get_datetime_list()
    date_index = dict([(d, i) for i, d in enumerate(refdates)])

    if axes is None:
        if new:
            axes = create_figure()
            kplot(kdata, axes=axes)
        else:
            axes = gca()

    ylim = axes.get_ylim()
    height = ylim[1] - ylim[0]

    if style == 1:
        arrow_buy = dict(arrowstyle="->")
        arrow_sell = arrow_buy
    else:
        arrow_buy = dict(facecolor='red', frac=0.5)
        arrow_sell = dict(facecolor='blue', frac=0.5)

    dates = sg.get_buy_signal()
    for d in dates:
        if d not in date_index:
            continue
        pos = date_index[d]
        krecord = kdata[pos]
        axes.annotate(
            'B', (pos, krecord.low - height * 0.01), (pos, krecord.low - height * 0.1),
            arrowprops=arrow_buy,
            horizontalalignment='center',
            verticalalignment='bottom',
            color='red'
        )

    dates = sg.get_sell_signal()
    for d in dates:
        if d not in date_index:
            continue
        pos = date_index[d]
        krecord = kdata[pos]
        axes.annotate(
            'S', (pos, krecord.high + height * 0.01), (pos, krecord.high + height * 0.1),
            arrowprops=arrow_sell,
            horizontalalignment='center',
            verticalalignment='top',
            color='blue'
        )




def sysplot(sys, new=True, axes=None, style=1):
    kdata = sys.to

    refdates = kdata.get_datetime_list()
    date_index = dict([(d, i) for i, d in enumerate(refdates)])

    if axes is None:
        if new:
            axes = create_figure()
            kplot(kdata, axes=axes)
        else:
            axes = gca()

    ylim = axes.get_ylim()
    height = ylim[1] - ylim[0]

    if style == 1:
        arrow_buy = dict(arrowstyle="->")
        arrow_sell = arrow_buy
    else:
        arrow_buy = dict(facecolor='red', frac=0.5)
        arrow_sell = dict(facecolor='blue', frac=0.5)

    tds = sys.tm.get_trade_list()
    buy_dates = []
    sell_dates = []
    for t in tds:
        if t.business == BUSINESS.BUY:
            buy_dates.append(t.datetime)
        elif t.business == BUSINESS.SELL:
            sell_dates.append(t.datetime)
        else:
            pass

    for d in buy_dates:
        if d not in date_index:
            continue
        pos = date_index[d]
        krecord = kdata[pos]
        axes.annotate(
            'B', (pos, krecord.low - height * 0.01), (pos, krecord.low - height * 0.1),
            arrowprops=arrow_buy,
            horizontalalignment='center',
            verticalalignment='bottom',
            color='red'
        )

    for d in sell_dates:
        if d not in date_index:
            continue
        pos = date_index[d]
        krecord = kdata[pos]
        axes.annotate(
            'S', (pos, krecord.high + height * 0.01), (pos, krecord.high + height * 0.1),
            arrowprops=arrow_sell,
            horizontalalignment='center',
            verticalalignment='top',
            color='blue'
        )
