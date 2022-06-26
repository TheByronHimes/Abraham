import re
import operator

gv = dict()
gv['i'] = 0
gv['tape'] = [0]
gv['buffer'] = []
gv['tokens'] = list()
gv['loopcons'] = list()
gv['loopactions'] = list()
gv['cval'] = 0
    
def mr():
    raw = gv['tokens'].pop()
    v = cast(getParmType(raw), raw)
    newIndex = gv['i'] + v
    if newIndex >= len(gv['tape']):
        gv['tape'].extend([0] * (newIndex + 1 - len(gv['tape'])))
    gv['i'] += v


def ml():
    raw = gv['tokens'].pop()
    v = cast(getParmType(raw), raw)
    gv['i'] -= v
    if gv['i'] < 0:
        raise Exception('moved off the end of the world')

def incr():
    raw = gv['tokens'].pop()
    v = cast(getParmType(raw), raw)
    gv['tape'][gv['i']] += v


def decr():
    raw = gv['tokens'].pop()
    v = cast(getParmType(raw), raw)
    gv['tape'][gv['i']] -= v


def getInput():
    x = input()
    x = cast(getParmType(x), x)
    gv['tape'][gv['i']] = x


def storeVal():
    raw = gv['tokens'].pop()
    v = cast(getParmType(raw), raw)
    gv['buffer'] = gv['buffer'][1:]
    gv['tape'][gv['i']] = v
    

def loop():
    rawOp = gv['tokens'].pop()
    rawVal = gv['tokens'].pop()
    ops = {'>':operator.gt, '<':operator.lt, '==':operator.eq}
    op = ops[rawOp]
    val = cast(getParmType(rawVal), rawVal)
    gv['loopcons'].append([op, val])
    
    # need to eval actions within loop
    actions = list()
    while gv['tokens'][-1] != 'loopend':
        actions.append(gv['tokens'].pop())
    actions.reverse()
    gv['loopactions'].append(actions.copy())
    

def loopend():
    op, val = gv['loopcons'][-1]
    condition_met = op(gv['tape'][gv['i']], val)
    
    if condition_met:
        # if loop conditions are met, re-append the loop actions
        gv['tokens'].append('loopend')
        gv['tokens'].extend(gv['loopactions'][-1])
        
    else:
        # if loop conditions aren't met, pop off that loop
        gv['loopcons'].pop()
        gv['loopactions'].pop()


def copyVal():
    gv['cval'] = gv['tape'][gv['i']]


def pasteVal():
    gv['tape'][gv['i']] = gv['cval']


def cast(typeString, val):
    d = dict()
    d['float'] = float
    d['int'] = int
    d['bool'] = bool
    d['str'] = str

    try:
        return d[typeString](val)
    except:
        raise Exception('Error converting value %s to type %s' % (val, typeString))


def getParmType(p):
    tokens = [
        ('float', r'\-?\d+\.\d*'),
        ('int', r'\-?\d+'),
        ('bool', r'True|False'),
        ('str', r'\".*\"')
    ]

    ms = re.compile('|'.join(['(?P<%s>%s)' % tup for tup in tokens]))

    match = re.match(ms, p)
    return match.lastgroup
    

def printCell():
    print(gv['tape'][gv['i']])


def processCond(match):
    s = match.string[match.start():match.end()]
    s = s[s.index('('):s.index(')')]
    cond = s[len('(But only when '):]
    
    # parse condition
    t = [
        ('gt', r'they had more than \d+ fish'),
        ('lt', r'they had less than \d+ fish'),
        ('deq', r'they had \d+ fish'),
        ('seq', r'the stone said \".*\"')
    ]

    op = ''
    val = ''
    ms = re.compile('|'.join(['(?P<%s>%s)' % tup for tup in t]))

    optype = re.search(ms, cond).lastgroup
    
    if optype in ['gt', 'lt', 'deq']:
        d = re.search(r'\d+', cond)
        if d:
            val = d.group()

    elif optype=='seq':
        op = '=='
        d = re.search(r'\".*\"')
        if d:
            val = d.group().strip('"')
            
    else:
        return 'error'

    opdict = {'deq':'==', 'seq':'==', 'gt':'>', 'lt':'<'}
    op = opdict[optype]

    return op, val
    


def processDigitToken(match):
    s = match.string[match.start():match.end()]
    ms = re.compile(r'\d+')
    m = re.search(ms, s)
    v = 0
    if m is not None:
        v = m.group()
    return v


def processStoreToken(match):
    s = match.string[match.start():match.end()]
    ms = re.compile(r'\".*\"')
    val = re.search(ms, s)
    return val.group()
    

def consumeToken(token):
    #print(gv['tape'])
    comms = dict()
    comms['mr'] = mr
    comms['ml'] = ml
    comms['incr'] = incr
    comms['decr'] = decr
    comms['store'] = storeVal
    comms['pin'] = getInput
    comms['pout'] = printCell
    comms['while'] = loop
    comms['loopend'] = loopend
    comms['copyval'] = copyVal
    comms['pasteval'] = pasteVal
    comms[token]()
          
          
def consumeTokenList():
    while len(gv['tokens']) > 0:
        consumeToken(gv['tokens'].pop())
        

def tokenize(s):
    t = [
        ('mr', r'Overhead, the geese flew \d* miles east\.'),
        ('ml', r'Overhead, the geese flew \d* miles west\.'),
        ('incr', r'He sold \d* sheep\.'),
        ('decr', r'They paid for their \d* mistakes\.'),
        ('pout', r'And Abraham spoke!'), 
        ('pin', r'He listened when his wife spoke\.'),
        ('while', r'He ran up into the mountains \(but only when.*\)\. This is what happened there\:'),
        ('loopend', r'Alas, I digress\.'),
        ('store', r'Preparing for the storm, he inscribed \".*\" into the stone\.'),
        ('copyval', r'One day he stole his neighbor\'s goods\.'),
        ('pasteval', r'He repented and returned the property\.'),
        ('s', r'\s+')
    ]

    ms = re.compile('|'.join(['(?P<%s>%s)' % tup for tup in t]))
    output = []
    lastend = 0
    f = [x for x in re.finditer(ms, s)]

    for m in f:
        if m.lastgroup == 's':
            lastend = m.end()
            continue
        
        if m.start() != lastend:
            output.append('error')
            return output
        
        if m.lastgroup in ['mr', 'ml', 'incr', 'decr']:
            output.append(m.lastgroup)   
            output.append(processDigitToken(m))
            
        elif m.lastgroup == 'store':
            output.append(m.lastgroup)   
            output.append(processStoreToken(m))
            
        elif m.lastgroup == 'while':
            output.append(m.lastgroup)
            output.extend(processCond(m))
            
        else:
            output.append(m.lastgroup)
        lastend = m.end()
        
    if lastend != len(s) and s[-1]!=' ':
        output.append('error')

    output.reverse()
    
    return output


def interpret(abraham_code, *args):
    gv['buffer'] = [a for a in args]
    test = 'Overhead, the geese flew 5 miles east. \
        Overhead, the geese flew 4 miles west. \
        Preparing for the storm, he inscribed "\'bananas\'" into the stone. \
        And Abraham spoke!'
        
    gv['tokens'] = tokenize(abraham_code)
    #print(gv['tokens'])
    consumeTokenList()


def processFile(fn):
    f = open(fn, 'r').read()
    interpret(f)


