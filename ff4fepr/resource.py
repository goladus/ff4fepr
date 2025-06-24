import os, yaml, csv, json

resource_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

def path(fname_or_pathlist):
    if isinstance(fname_or_pathlist, list):
        pathlist=[resource_dir] + fname_or_pathlist
        return os.path.join(*pathlist)
    else:
        return os.path.join(resource_dir, fname_or_pathlist)

def isfloat(strng):
    return not False in [x.isdigit() for x in strng.split('.')]

def int_ints(strng):
    'make int if string isdigit, otherwise return string'
    if strng == '':
        return None
    if strng.startswith('0x'):
        return int(strng, 16)
    if strng == 'nothing':
        return 'EMPTY'
    if strng.isdigit():
        return int(strng)
    elif isfloat(strng):
        return float(strng)
    else:
        return strng

def intify(row):
    return [int_ints(x) for x in row]

def csv_dumper(file_handle, data, header_row=True):
    header=data['header']
    rows=data['rows']
    writer=csv.writer(file_handle)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

def csv_loader(file_handle, header_row=True):
    data=list(csv.reader(file_handle))
    if data[0][0]=='TABLE':
        return {'header': data[0][1:],
                'rows': [intify(row) for row in data[1:]]}
    else:
        if header_row:
            return {'header': data[0],
                    'rows': [intify(row) for row in data[1:]]}
        else:
            return data

def yml_loader(file_handle):
    return yaml.safe_load(file_handle)

def json_loader(file_handle):
    return json.load(file_handle)

def lst_loader(file_handle):
    return [x.strip() for x in handle(resource_name, 'lst').readlines() if x.strip() != '']

loaders = {
    'csv': csv_loader,
    'yml': yml_loader,
    'yaml': yml_loader,
    'json': json_loader,
    'lst': lst_loader,
    }

def handle(fname):
    return open(path(fname), 'r')

def load_file(resource_file_name, resource_name=None):
    if resource_name is None:
        resource_name=resource_file_name.split('.')[0]
    extension=resource_file_name.split('.')[-1:][0]
    if (extension==resource_name) and (len(extension) == len(resource_file_name)):
        return None
    if os.path.isfile(path(resource_file_name)):
        return loaders[extension](open(resource_file_name, 'r'))
    else:
        return None

def loadable(fname):
    return True in [fname.endswith(extension) for extension in list(loaders.keys())]

def dirlist(dirpath):
    return [x for x in os.listdir(os.path.abspath(dirpath)) if loadable(x)]

def load(resource_name, resourcedir=resource_dir):
    lst=[f for f in dirlist(resourcedir) if f.split('.')[0] == resource_name]
    if len(lst) > 1:
        sys.stderr.write('warning, multiple resource files found: %s\n' % ', '.join(lst))
    resource_file_name=lst[0]
    loader=load_file(path(resource_file_name))
    if loader is None:
        if os.path.isdir(path(resource_file_name)):
            return dir_loader(path(resource_file_name))
        else:
            sys.stderr.write('invalid resource file')
    else:
        return loader
