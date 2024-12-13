# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/12/12 19:09:22
@Author  :   chaopaoo12
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib
import pandas as pd


def SQL_CREATE_STATEMENT_FROM_DATAFRAME(SOURCE, TABLE_NAME):
    sql_text = pd.io.sql.get_schema(SOURCE, TABLE_NAME)
    return (sql_text)
