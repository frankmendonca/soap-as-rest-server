class XmlConverter:
    def __init__(self, prefix, method, params):
        self.text = ''
        self.prefix = prefix
        self.method = method
        self.params = params

    def create_tag(self, parent, elem):
        if isinstance(elem, dict):
            for key, value in elem.items():
                self.text += f'<{self.prefix}:{key}>'
                self.create_tag(key, value)
                self.text += f'</{self.prefix}:{key}>'
        elif isinstance(elem, list):
            for value in elem:
                self.create_tag(parent, value)
        else:
            self.text += f'{elem}'

    def build_body(self):
        self.text += f'<{self.prefix}:{self.method}Request>'
        self.create_tag(None, self.params)
        self.text += f'</{self.prefix}:{self.method}Request>'
        return self.text


def convert_json_to_xml(prefix, method, params):
    s = XmlConverter(prefix, method, params)
    return s.build_body()
