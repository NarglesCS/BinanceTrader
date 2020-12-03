#ls_ma_interval = [2,4,6,12,24,48,336,1344]
ls_ma_interval = [2,4,6,16,24,48,336]
map_ma = {
    2:[],
    4:[],
    6:[],
    16:[],
    24:[],
    48:[],
    336:[]
}
def update_map(ma):
    for i in ls_ma_interval:
        map_ma[i].append(get_moving_average(ma[-i:]))
    return map_ma
def get_moving_average(cs):
    sum =0.0
    for i in cs:
        sum += float(i[4])
    ma = sum/len(cs)
    return ma
def get_slope(ls_ma):
    return 0
def get_cur_ma(ma):
    return ma[-1]
def get_prev_ma(ma):
    return ma[-2]
