from llmbroker import Query


def get_draw_title(kdata):
    
    if not kdata:
        return ""

    query = kdata.get_query()
    stock = kdata.get_stock()
    if stock.is_null():
        return ""

    s1 = ''
    if query.ktype == Query.DAY:
        s1 = u' （日线）'
    elif query.ktype == Query.WEEK:
        s1 = u' （周线）'
    elif query.ktype == Query.MONTH:
        s1 = u' （月线）'
    elif query.ktype == Query.QUARTER:
        s1 = u' （季线）'
    elif query.ktype == Query.HALFYEAR:
        s1 = u' （半年线）'
    elif query.ktype == Query.YEAR:
        s1 = u' （年线）'
    elif query.ktype == Query.MIN:
        s1 = u' （1分钟线）'
    elif query.ktype == Query.MIN5:
        s1 = u' （5分钟线）'
    elif query.ktype == Query.MIN15:
        s1 = u' （15分钟线）'
    elif query.ktype == Query.MIN30:
        s1 = u' （30分钟线）'
    elif query.ktype == Query.MIN60:
        s1 = u' （60分钟线）'

    name = stock.name

    if stock.code == "":
        stitle = "Block(%s) %s" % (stock.id, name) + s1
    else:
        stitle = stock.market + stock.code + ' ' + name + s1

    return stitle