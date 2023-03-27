import ast

from pyzabbix import ZabbixAPI  # 1.1.7
from pyzabbix import api


class Zabbix:

    number_of_added_hosts = 0
    number_of_notadded_hosts = 0

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.z = ZabbixAPI(self.url, user=self.user, password=self.password)

    def connection_check(self) -> bool:
        try:
            answer = self.z.do_request('apiinfo.version')
            if answer:
                return True
        except Exception as err:
            raise Exception(err)

    def adding_hosts(self, hosts_list) -> [str, True]:

        try:
            result = self.z.host.create(hosts_list)
            self.number_of_added_hosts += 1
            return True
        except api.ZabbixAPIException as err:
            self.number_of_notadded_hosts += 1
            error = ast.literal_eval(str(err))
            return f"ERROR host - {hosts_list['host']}   {error['message']}   {error['data']}"

    def group(self) -> list:
        groups = []
        z_groups = self.z.hostgroup.get(output=('groupid', 'name'))
        for group in z_groups:
            groups.append({'group_name': group['name'], 'group_id': group['groupid']})
        return groups

    def templates(self) -> list:
        templates = []
        z_templates = self.z.template.get(output=('host', 'templateid'))
        for template in z_templates:
            templates.append({'template_name': template['host'], 'template_id': template['templateid']})
        return templates

    def proxy(self) -> list:
        proxies = []
        z_proxies = self.z.proxy.get(output=('host', 'proxyid'))
        for proxy in z_proxies:
            proxies.append({'proxy_name': proxy['host'], 'proxy_id': proxy['proxyid']})
        return proxies
