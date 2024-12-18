# -*- encoding: utf-8 -*-
'''
@File    :   fetch_record.py
@Time    :   2024/12/13 13:33:26
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib
from Eccang.eccang_base import eccang


def getListingSummaryOriginal(path='setting.json', end_date=None, create_date=None):
    # listing表现-日维度接口
    EC = eccang(path)
    ListingSummaryOriginal = EC.get_data(interface_name='ListingSummaryOriginal',
                                         biz_content={'page':1,'page_size':1000,
                                                      'start_time':create_date,
                                                      'end_time':end_date},
                                         data_format='dataframe')
    return (ListingSummaryOriginal)


def getPurchaseOrders(path='setting.json', end_datetime=None, create_datetime=None, update_datetime=None):
    # 采购单 *********
    EC = eccang(path)
    if create_datetime is not None:
        # 采购单 创建
        PurchaseOrders = EC.get_data(interface_name='getPurchaseOrders',
                                     biz_content={'page':1,'page_size':100,
                                                  'search_date_type':'createDate',
                                                  'date_for':create_datetime,
                                                  'date_to':end_datetime},
                                     data_format='dataframe')
    elif update_datetime is not None:
        # 采购单 刷新状态
        PurchaseOrders = EC.get_data(interface_name='getPurchaseOrders',
                                     biz_content={'page':1,'page_size':100,
                                                  'search_date_type':'updateTime',
                                                  'date_for':update_datetime,
                                                  'date_to':end_datetime},
                                     data_format='dataframe')
    return (PurchaseOrders)


def getTransferOrders(path='setting.json', end_datetime=None, create_datetime=None, modify_datetime=None, receiving_datetime=None):
    # 调拨单 最长查一个月
    EC = eccang(path)
    if create_datetime is not None:
        TransferOrders = EC.get_data(interface_name='getTransferOrders', 
                                    biz_content={'page':1,'page_size':100,
                                                'date_create_for':create_datetime,
                                                'date_create_to':end_datetime},
                                    data_format='dataframe')
    elif modify_datetime is not None:
        TransferOrders = EC.get_data(interface_name='getTransferOrders', 
                                    biz_content={'page':1,'page_size':100,
                                                'date_last_modify_for':modify_datetime,
                                                'date_last_modify_to':end_datetime},
                                    data_format='dataframe')
    elif receiving_datetime is not None:
        TransferOrders = EC.get_data(interface_name='getTransferOrders', 
                                    biz_content={'page':1,'page_size':100,
                                                'data_receiving_for':receiving_datetime,
                                                'data_receiving_to':end_datetime},
                                    data_format='dataframe')
    return (TransferOrders)


def getReceiving(path='setting.json', end_datetime=None, create_datetime=None, update_datetime=None):
    # 入库单
    EC = eccang(path)
    if create_datetime is not None:
        Receiving = EC.get_data(interface_name='getReceiving', 
                                biz_content={'page':1,'page_size':100,
                                            'search_date_type':'receiving_add_time',
                                            'date_for':create_datetime,
                                            'date_to':end_datetime},
                                data_format='dataframe')
    elif update_datetime is not None:
        Receiving = EC.get_data(interface_name='getReceiving', 
                                biz_content={'page':1,'page_size':100,
                                            'search_date_type':'receiving_update_time',
                                            'date_for':update_datetime,
                                            'date_to':end_datetime},
                                data_format='dataframe')
    return (Receiving)


def getPutAwayList(path='setting.json', end_date=None, start_date=None, put_date=None):
    # 上架单
    EC = eccang(path)
    if start_date is None:
        PutAwayList = EC.get_data(interface_name='getPutAwayList',
                                biz_content={'page':1,'page_size':50,
                                            'date_type':1,
                                            'start_date':start_date,
                                            'end_date':end_date}, 
                                data_format='dataframe')
    elif put_date is None:
        PutAwayList = EC.get_data(interface_name='getPutAwayList',
                                biz_content={'page':1,'page_size':50,
                                            'date_type':2,
                                            'start_date':put_date,
                                            'end_date':end_date}, 
                                data_format='dataframe')
    return (PutAwayList)


def getDeliveryDetailList(path='setting.json', end_datetime=None, start_datetime=None):
    # 出库明细 
    EC = eccang(path)
    DeliveryDetailList = EC.get_data(interface_name='getDeliveryDetailList',
                                     biz_content={'page':1,'page_size':100,
                                                  'date_for':start_datetime,
                                                  'date_to':end_datetime},
                                     data_format='dataframe')
    return (DeliveryDetailList)


def getOrderList(path='setting.json', end_datetime=None, 
                 create_datetime=None, update_datetime=None, ship_datetime=None,
                 paid_datetime=None, delivered_datetime=None):
    # 订单列表
    EC = eccang(path)
    if create_datetime is not None:
        OrderList = EC.get_data(interface_name='getOrderList',
                            biz_content={'page':1,'page_size':100,
                                         'get_detail':1,'get_address':1,
                                         'get_custom_order_type':1,
                                         'condition':{'created_date_start':create_datetime,
                                                      'created_date_end':end_datetime}},
                            data_format='dataframe')
    elif update_datetime is not None:
        OrderList = EC.get_data(interface_name='getOrderList',
                            biz_content={'page':1,'page_size':100,
                                         'get_detail':1,'get_address':1,
                                         'get_custom_order_type':1,
                                         'condition':{'update_date_start':update_datetime,
                                                      'update_date_end':end_datetime}},
                            data_format='dataframe')
    elif ship_datetime is not None:
        OrderList = EC.get_data(interface_name='getOrderList',
                            biz_content={'page':1,'page_size':100,
                                         'get_detail':1,'get_address':1,
                                         'get_custom_order_type':1,
                                         'condition':{'ship_date_start':ship_datetime,
                                                      'ship_date_end':end_datetime}},
                            data_format='dataframe')
    elif paid_datetime is not None:
        OrderList = EC.get_data(interface_name='getOrderList',
                            biz_content={'page':1,'page_size':100,
                                         'get_detail':1,'get_address':1,
                                         'get_custom_order_type':1,
                                         'condition':{'platform_paid_date_start':paid_datetime,
                                                      'platform_paid_date_end':end_datetime}},
                            data_format='dataframe')
    elif delivered_datetime is not None:
        OrderList = EC.get_data(interface_name='getOrderList',
                            biz_content={'page':1,'page_size':100,
                                         'get_detail':1,'get_address':1,
                                         'get_custom_order_type':1,
                                         'condition':{'track_delivered_time_start':delivered_datetime,
                                                      'track_delivered_time_end':end_datetime}},
                            data_format='dataframe')
    return (OrderList)


def getRmaReturnList(path='setting.json', end_datetime=None, create_datetime=None):
    # 退货列表
    EC = eccang(path)
    ReturnList = EC.get_data(interface_name='getRmaReturnList', 
                             biz_content={'page':1,'page_size':100,
                                          'create_date_start':create_datetime,
                                          'create_date_end':end_datetime},
                             data_format='dataframe')
    return (ReturnList)


def getShipBatch(path='setting.json', user_id=None, end_date=None, create_date=None, update_date=None):
    # 头程数据
    #todo: userid传入
    EC = eccang(path)
    if create_date is not None:
        ShipBatch = EC.get_data(interface_name='getShipBatch',
                                biz_content={'page':1,'page_size':1000,
                                            'user_id':user_id,
                                            'date_for':create_date,
                                            'date_to':end_date},
                                data_format='dataframe')
    elif update_date is not None:
        ShipBatch = EC.get_data(interface_name='getShipBatch',
                                biz_content={'page':1,'page_size':1000,
                                            'user_id':user_id,
                                            'update_for':update_date,
                                            'update_to':end_date},
                                data_format='dataframe')
    return (ShipBatch)


def getProductInventory(path='setting.json', end_date=None, update_date=None):
    # 即时库存
    EC = eccang(path)
    ProductInventory = EC.get_data(interface_name='getProductInventory',
                                   biz_content={'page':1,'page_size':100,
                                                'update_time_from':update_date,
                                                'update_time_to':end_date} ,
                                   data_format='dataframe')
    return (ProductInventory)


def getInventoryBatch(path='setting.json', end_date=None, create_date=None, update_date=None):
    # 头程数据
    EC = eccang(path)
    if create_date is not None:
        InventoryBatch = EC.get_data(interface_name='getInventoryBatch',
                                     biz_content={'page':1,'page_size':1000,
                                                'fifo_time_from':create_date,
                                                'fifo_time_to':end_date},
                                    data_format='dataframe')
    elif update_date is not None:
        InventoryBatch = EC.get_data(interface_name='getInventoryBatch',
                                    biz_content={'page':1,'page_size':1000,
                                                'fifo_time_from':update_date,
                                                'fifo_time_to':end_date},
                                    data_format='dataframe')
    return (InventoryBatch)
