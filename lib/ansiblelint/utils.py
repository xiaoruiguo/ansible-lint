import os
import glob
import imp

def matchlines(text, fn):
    result = []
    # arrays are 0-based, line numbers are 1-based
    # so use prev_line_no as the counter 
    for (prev_line_no, line) in enumerate(text.split("\n")):
        if fn(line):
            result.append(prev_line_no+1)
    return result

def load_plugins(directory):
    result = []
    fh = None

    for pluginfile in glob.glob(os.path.join(directory, '[A-Za-z]*.py')):

        pluginname = os.path.basename(pluginfile.replace('.py', ''))
        try:
            fh, filename, desc = imp.find_module(pluginname, [directory])
            mod = imp.load_module(pluginname, fh, filename, desc)
            obj = getattr(mod, pluginname)()
            result.append(obj)
        finally:
            if fh:
                fh.close()
    return result


def tokenize(line):
    tokens = line.lstrip().split(" ")
    if tokens[0] == 'action:': 
        tokens = tokens[1:]
    key = tokens[0].replace(":", "")
    args = dict()
    for arg in tokens[1:]:
        kv = arg.split("=",1) 
        # make rhs of = blank if not set
        # http://stackoverflow.com/questions/2492087
        args[kv[0]] = (kv[1:] or [''])[0]
    return (key, args)