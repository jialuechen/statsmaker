import struct
import pathlib

from .common_mysql import get_marketid

def llmbroker_import_weight(connect, src_dir, market):
    cur = connect.cursor()

    marketid = get_marketid(connect, market)

    src_path = pathlib.Path(src_dir + '/shase/weight') if market == 'SH' else pathlib.Path(src_dir + '/sznse/weight')
    wgt_file_list = list(src_path.glob('*.wgt'))

    records = []
    for wgt_file in wgt_file_list:
        code = wgt_file.stem
        cur.execute("select stockid from `llmbroker_base`.`stock` where marketid=%s and code='%s'" % (marketid, code))
        stockid = [id[0] for id in cur.fetchall()]
        if not stockid:
            continue

        with wgt_file.open('rb') as sourcefile:
            stockid = stockid[0]
            cur.execute("select date from `llmbroker_base`.`stkweight` where stockid=%s" % stockid)
            dateDict = dict([(i[0], None) for i in cur.fetchall()])


            data = sourcefile.read(36)
            while data:
                a = struct.unpack('iiiiiiiii', data)
                date = (a[0] >> 20) * 10000 + (((a[0] << 12) & 4294967295) >> 28) * 100 + ((a[0] & 0xffff) >> 11)
                if date not in dateDict\
                        and a[0] >= 0 and a[1] >= 0 and a[2] >= 0 and a[3] >= 0 and a[4] >= 0\
                        and a[5] >= 0 and a[6] >= 0 and a[7] >= 0:
                    records.append((stockid, date, a[1], a[2], a[3], a[4], a[5], a[6], a[7]))
                data = sourcefile.read(36)
            sourcefile.close()

    if records:
        cur.executemany("INSERT INTO `llmbroker_base`.`stkweight` (stockid, date, countAsGift, \
                         countForSell, priceForSell, bonus, countOfIncreasement, totalCount, freeCount) \
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        records)

    connect.commit()
    cur.close()
    return len(records)
