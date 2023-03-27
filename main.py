import pandas as pd
import json_preparation as js_prepare
import zabbix_functions as zab_func
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def main(server: str, login: str, pas: str, file: str) -> None:
    connecting = None

    try:
        connecting = zab_func.Zabbix(server, login, pas)
        connecting.connection_check()
    except Exception as err:
        print(err)
        ...
    else:
        print('connected to zabbix_api')

    # this is the block of received data stored in variables
    gr = connecting.group()
    tmp = connecting.templates()
    prx = connecting.proxy()

    df = pd.read_excel(f'{file}', dtype={'technical_name': str}, sheet_name=0).fillna(0)

    for enum, items in df.iterrows():
        hosts = js_prepare.FormatJson_preparation(items, tmp, gr, prx)  # creating the class object
        prepare_data = hosts.functions_call()  # format json to add to zabbix
        result = connecting.adding_hosts(prepare_data)  # result of adding hosts to zabbix
        if result is not True:
            print(result)
    print(f'\n\nnumber of successfully added hosts  {connecting.number_of_added_hosts}')
    print(f'number of unsuccessfully added hosts  {connecting.number_of_notadded_hosts}')


if __name__ == '__main__':

    # dotenv .env
    main(
        os.environ.get("zabbix_server"),
        os.environ.get("zabbix_login"),
        os.environ.get("zabbix_pass"),
        os.path.join(os.getcwd(), os.environ.get("file_name"))
    )