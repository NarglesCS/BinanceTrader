import stats

def ma_buy_sig(map_ma, trend, pred, risk):
    if ((stats.get_cur_ma(map_ma[trend])) >= (stats.get_cur_ma(map_ma[pred]))) & ((stats.get_prev_ma(map_ma[trend])) <= (stats.get_prev_ma(map_ma[pred]))) & (not risk):
        return True
    return False
def ma_sell_sig(map_ma, trend, pred, risk):
    if ((stats.get_cur_ma(map_ma[trend])) <= (stats.get_cur_ma(map_ma[pred]))) & ((stats.get_prev_ma(map_ma[trend])) >= (stats.get_prev_ma(map_ma[pred]))) & (risk):
        return True
    return False
