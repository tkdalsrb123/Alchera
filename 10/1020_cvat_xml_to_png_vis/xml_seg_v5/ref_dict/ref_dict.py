
def ref_dict(_dict, address_l):
    _curr = _dict
    for add in address_l:
        if type(add) is int:
            if type(_curr) is not list:
                # print('_curr is not list')
                return []
            if add >= len(_curr):
                # print('index is out of range')
                return []
            _curr = _curr[add]
        elif type(add) is str:
            if type(_curr) is not dict:
                # print('_curr is not dict')
                return []
            _curr = _curr.get(add, '')
      
    return _curr