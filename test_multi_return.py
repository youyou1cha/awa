# 使用dict
def latlon_to_address(lat,lon):
    return {
        'country':'country',
        'province':'province',
        'city':'city'
    }

addr_dict = latlon_to_address(lat='lat',lon='lon')

# 使用namedtuple

from collections import namedtuple

Address = namedtuple("Address",['country','province','city'])

def latlon_to_address(lat,lon):
    return Address(
        country='country',
        province='province',
        city='city'
    )
addr = latlon_to_address(lat='lat',lon='lon')