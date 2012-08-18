import os
from yaml import load


grammar_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grammarish.yml')
DEFAULT_GRAMMARISH = load(open(grammar_file, 'r'))

def simple_quote(s):
    if isinstance(s, basestring):
        value = "'{}'".format(s)
        return value
    return s

def generate_source(source, grammar=DEFAULT_GRAMMARISH):
    global pysrc
    pysrc = ""
    indent = 0
    def add_line(s):
        global pysrc
        pysrc += "{}{}\n".format(' ' * 4 * indent, s)
    for model, info in source.items():
        add_line("class {}(models.Model):".format(model))
        indent += 1
        try:
            docs = info.pop('doc')
            add_line('''"""{}"""'''.format(docs))
            pysrc += '\n'
        except KeyError:
            pass
        for field, fdata in info.items():
            if '-' in field:
                field, the_type = [s.strip() for s in field.split('-')]
            else:
                the_type = fdata.pop('type')
            field_type = grammar['types'][the_type]
            add_line("{} = models.{}(".format(field, field_type))
            indent += 1
            args = fdata.pop('args', [])
            if not isinstance(args, list):
                if ',' in args:
                    args = args.split(',')
                else:
                    args = [args]
            for arg in args:
                add_line('{},'.format(simple_quote(arg)))
            field_info = grammar['defaults'].get(the_type, {}).copy()
            field_info.update(fdata)
            for kwarg, value in field_info.items():
                add_line("{}={},".format(kwarg, simple_quote(value)))
            pysrc = pysrc.rstrip(',\n)')
            pysrc += ')\n'
            indent -= 1
        pysrc += '\n'
        indent -= 1
    return pysrc



