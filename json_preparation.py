class FormatJson_preparation:
    __slots__ = {'df','tmp','grp','prx'}
    add_dic = {}

    def __init__(self, df, templates, groups, proxies):
        self.df = df
        self.tmp = templates
        self.grp = groups
        self.prx = proxies

    def technical_name(self):
        self.add_dic['host'] = self.df['technical_name']

    def visible_name(self):
        if self.df['visible_name']:
            self.add_dic['name'] = self.df['visible_name']

    def interface(self):
        if self.df['interface'] == 'agent':
            self.add_dic['interfaces'] = [
                {'type': 1, 'main': '1', 'useip': '1', 'ip': self.df['ip_adress'], 'dns': '', 'port': '10050'}]
        elif self.df['interface'] == 'snmp':
            self.add_dic['interfaces'] = [
                {'type': 2, 'main': '1', 'useip': '1', 'details': {'version': '2', 'community': '{$SNMP_COMMUNITY}'},
                 'ip': self.df['ip_adress'], 'dns': '', 'port': '161'}]

    def groups(self):
        self.add_dic['groups'] = [{'groupid': f} for f in
                                  [i['group_id'] for i in self.grp if i['group_name']
                                   in self.df['groups'].split(';')]]

    def templates(self):
        if self.df['templates']:
            self.add_dic['templates'] = [{'templateid': f} for f in
                                         [i['template_id'] for i in self.tmp if i['template_name']
                                          in self.df['templates'].split(';')]]

    def description(self):
        if self.df['description']:
            self.add_dic['description'] = self.df['description']

    def proxy(self):
        if self.df['proxy']:
            proxy = [i['proxy_id'] for i in self.prx if self.df['proxy'] in i['proxy_name']][0]
            self.add_dic['proxy_hostid'] = proxy

    def status(self):
        if self.df['status'] == 'deactivate':
            self.add_dic['status'] = '1'
        if self.df['status'] == 'activate':
            self.add_dic['status'] = '0'

    def tags(self):
        if self.df['tags']:
            tags = []
            for i in self.df['tags'].split(';'):
                tags.append({'tag': i.split('=')[0], 'value': i.split('=')[1]})
            self.add_dic['tags'] = tags

    def macros(self):
        if self.df['macros']:
            macros = []
            for i in self.df['macros'].split(';'):
                macros.append({'macro': i.split('=')[0], 'value': i.split('=')[1]})

            self.add_dic['macros'] = macros

            # self.df['templates']

    def functions_call(self) -> dict:
        self.add_dic.clear()
        self.technical_name()
        self.groups()
        self.templates()
        self.visible_name()
        self.interface()
        self.description()
        self.proxy()
        self.status()
        self.tags()
        self.macros()

        return self.add_dic
