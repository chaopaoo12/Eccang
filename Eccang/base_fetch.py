# -*- encoding: utf-8 -*-
'''
@File    :   base_fetch.py
@Time    :   2024/12/13 11:18:57
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib

from Eccang.Eccang.eccang_base import eccang


def getWarehouseList(path='setting.json'):
    # 获取仓库列表
    EC = eccang(path)
    WarehouseList = EC.get_data(interface_name='getWarehouseList', biz_content={'page':1,'page_size':100}, data_format='dataframe')
    return (WarehouseList)


def getWarehousesInfo(path='setting.json'):
    # 获取仓库信息
    EC = eccang(path)
    Warehouses_info = EC.get_data(interface_name='getWarehouses', biz_content={'page':1,'page_size':100}, data_format='dataframe')
    return (Warehouses_info)


def getWarehouseShippingForOrder(path='setting.json'):
    # 获取仓库配送方式
    EC = eccang(path)
    WarehouseShippingForOrder = EC.get_data(interface_name='getWarehouseShippingForOrder', biz_content={'page':1,'page_size':100}, data_format='json')
    return (WarehouseShippingForOrder)


def getShippingMethod(path='setting.json'):
    # 获取配送方式
    EC = eccang(path)
    ShippingMethod = EC.get_data(interface_name='getShippingMethod', biz_content={'page':1,'page_size':100}, data_format='json')
    return (ShippingMethod)


def getProductCategoryBase(path='setting.json'):
    # 品类列表
    EC = eccang(path)
    ProductCategoryBase = EC.get_data(interface_name='getProductCategoryBase', biz_content={'page':1,'page_size':100}, data_format='json')
    return (ProductCategoryBase)


def getSupplier(path='setting.json'):
    # 供应商
    EC = eccang(path)
    res = EC.get_data(interface_name='getSupplier', biz_content={'page':1,'page_size':2}, data_format='json')
    for k, v in res[0].items():
        v['code'] = k
    import pandas as pd
    return pd.DataFrame(res[0].values())


def getWmsProductList(path='setting.json', end_date=None, create_date=None):
    # wms产品列表
    EC = eccang(path)
    WmsProductList = EC.get_data(interface_name='getWmsProductList',
                                 biz_content={'page':1,'page_size':1000,
                                              'product_add_time_from':create_date,
                                              'product_add_time_to':end_date},
                                 data_format='dataframe')
    return (WmsProductList)


def getAmazonListing(path='setting.json', end_date=None, create_date=None, update_date=None):
    # 亚马逊listing列表
    EC = eccang(path)
    if create_date is not None:
        # 亚马逊listing 创建
        AmazonListing = EC.get_data(interface_name='AmazonListing',
                                    biz_content={'page':1,'page_size':100,
                                                'open_date_local_start':create_date,
                                                'open_date_local_end':end_date},
                                    data_format='dataframe')
    elif update_date is not None:
        # 亚马逊listing 更新
        AmazonListing = EC.get_data(interface_name='AmazonListing',
                                    biz_content={'page':1,'page_size':100,
                                                'updated_time_start':update_date,
                                                'updated_time_end':end_date},
                                    data_format='dataframe')
    return (AmazonListing)


def getUserAccountList(path='setting.json', platform='amazon'):
    # 店铺列表
    EC = eccang(path)
    UserAccountList = EC.get_data(interface_name='getUserAccountList',
                                  biz_content={'page':1,'page_size':1000,
                                               'platform':platform},
                                  data_format='dataframe')
    return (UserAccountList)


def getAuthAdStoreSiteList(path='setting.json'):
    # 获取有广告数据的店铺列表
    EC = eccang(path)
    AuthAdStoreSiteList = EC.get_data(interface_name='GetAuthAdStoreSiteList',
                                      biz_content={'page':1,'page_size':1000}, data_format='dataframe')
    return (AuthAdStoreSiteList)



