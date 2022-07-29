import re
import operator


rs = {
    'number': '((\-?\d+\.\d*)|(\-?\d+))',
    'bool': 'True|False',
    'string': '\".*\"'
}


class Interpreter:

    def __init__(self):
        self.i = 0
        self.tape = [0]
        self.buffer = []
        self.tokens = list()
        self.loopcons = list()
        self.loopactions = list()
        self.currentlooplevel = 0
        self.cval = 0
        self.output = ''
        self.has_error = False
        self.error = ''

    
    def mr(self):
        raw = self.tokens.pop()
        v = self.cast(getParmType(raw), raw)
        self.i += v
        length = len(self.tape) - 1
        if self.i > length:
            for n in range(length, self.i + 1):
                self.tape.append(0)


    def ml(self):
        raw = self.tokens.pop()
        v = self.cast(self.getParmType(raw), raw)
        self.i -= v
        if self.i < 0:
            self.has_error = True


    def incr(self):
        raw = self.tokens.pop()
        v = self.cast(self.getParmType(raw), raw)
        self.tape[self.i] += v


    def decr(self):
        raw = self.tokens.pop()
        v = self.cast(self.getParmType(raw), raw)
        self.tape[self.i] -= v


    def getInput(self):
        x = input()
        x = self.cast(self.getParmType(x), x)
        self.tape[self.i] = x


    def storeVal(self):
        raw = self.tokens.pop()
        v = self.cast(self.getParmType(raw), raw)
        self.buffer = self.buffer[1:]
        self.tape[self.i] = v


    def doLoop(self):
        raw = self.tokens.pop()
        loop_id = self.cast(self.getParmType(raw), raw)

        # get conditions linked to this loop
        op, val = self.loopcons[loop_id]
        condition_met = op(self.tape[self.i], val)

        # if conditions are met, push the loop actions onto the tokens stack
        if condition_met:
            self.tokens.extend(self.loopactions[loop_id])


    def defineLoop(self):

        # get the loop condition's operator (rawOp) and value (rawVal)
        rawOp = self.tokens.pop()
        rawVal = self.tokens.pop()
        ops = {'>':operator.gt, '<':operator.lt, '==':operator.eq}

        # dict with string as key and function as value
        op = ops[rawOp]
        val = self.cast(self.getParmType(rawVal), rawVal)

        # add the loop condition to the loop condition stack
        self.loopcons.append([op, val])
        loopIndex = len(self.loopactions)
        self.currentlooplevel += 1
        is_inner_loop = self.currentlooplevel > 1  # outermost loop will have loop level 1

        # need to evaluate actions within loop
        self.loopactions.append(list())
        while True:
            if self.tokens[-1] == 'while':
                self.tokens.pop()
                self.loopactions[loopIndex].extend(defineLoop())  # include tokens for any inner loops
            if self.tokens[-1] == 'loopend':
                # can either be loopend token for inner loop or for this loop
                self.tokens.pop()
                break  # either way, exit while loop
            else:
                # append normal token to list of actions for this loop
                self.loopactions[loopIndex].append(self.tokens.pop())

        # when we get to the end of the loop actions, re-evaluate loop condition
        self.loopactions[loopIndex].append('loop')
        self.loopactions[loopIndex].append(str(loopIndex))  # adds loop to end of itself for re-eval
        self.loopactions[loopIndex].reverse()

        self.currentlooplevel -= 1

        if is_inner_loop:  # all inner loops will return their loop token to containing loop
            return ['loop', str(loopIndex)]
        else:  # is base-level loop, so push on loop tokens for stack
            self.tokens.append(str(loopIndex))
            self.tokens.append('loop')


    def loopend(self):
        op, val = self.loopcons[-1]
        condition_met = op(self.tape[self.i], val)

        if condition_met:
            # if loop conditions are met, re-append the loop actions
            self.tokens.append('loopend')
            self.tokens.extend(self.loopactions[-1])


    def copyVal(self):
        self.cval = self.tape[self.i]


    def pasteVal(self):
        self.tape[self.i] = self.cval


    def cast(self, typeString, val):
        d = dict()
        d['float'] = float
        d['int'] = int
        d['bool'] = bool
        d['str'] = str

        try:
            if typeString == 'str':
                val = val.strip('"')
            return d[typeString](val)
        except:
            self.has_error = True


    def getParmType(self, p):
        tokens = [
            ('float', r'\-?\d+\.\d*'),
            ('int', r'\-?\d+'),
            ('bool', r'%s' % rs['bool']),
            ('str', r'%s' % rs['string'])
        ]

        ms = re.compile('|'.join(['(?P<%s>%s)' % tup for tup in tokens]))

        match = re.match(ms, p)
        return match.lastgroup


    def printCell(self):
        self.output += str(self.tape[self.i]) + '\n'


    def processCond(self, match):
        s = match.string[match.start():match.end()]
        s = s.replace('He ran into the mountains, but only when ', '')
        cond = s.replace('. This is what happened there:', '')

        # parse condition
        t = [
            ('gt', r'they had more than %s fish' % rs['number']),
            ('lt', r'they had less than %s fish' % rs['number']),
            ('eq', r'the stone said .*')
        ]

        op = ''
        val = ''
        ms = re.compile('|'.join(["(?P<%s>%s)" % tup for tup in t]))

        optype = re.search(ms, cond).lastgroup

        if optype in ['gt', 'lt', 'deq']:
            d = re.search(r'%s' % rs['number'], cond)
            if d:
                val = d.group()

        elif optype=='eq':
            op = '=='
            val = cond.replace('the stone said ', '')

        else:
            self.has_error = True
            return 'error'


        opdict = {'eq':'==', 'gt':'>', 'lt':'<'}
        op = opdict[optype]
        return op, val



    def processDigitToken(self, match):
        s = match.string[match.start():match.end()]
        ms = re.compile(r'%s' % rs['number'])
        m = re.search(ms, s)
        v = 0
        if m is not None:
            v = m.group()
        return v


    def processStoreToken(self, match):
        s = match.string[match.start():match.end()]
        s = s.replace('Preparing for the storm, he carved ', '')
        s = s.replace(' into the stone.', '')
        return s


    def consumeToken(self, token):
        comms = dict()
        comms['mr'] = self.mr
        comms['ml'] = self.ml
        comms['incr'] = self.incr
        comms['decr'] = self.decr
        comms['store'] = self.storeVal
        comms['pin'] = self.getInput
        comms['pout'] = self.printCell
        comms['while'] = self.defineLoop
        comms['loop'] = self.doLoop
        comms['loopend'] = self.loopend
        comms['copyval'] = self.copyVal
        comms['pasteval'] = self.pasteVal
        comms[token]()


    def consumeTokenList(self):
        while len(self.tokens) > 0:
            if self.has_error:
                break
            self.consumeToken(self.tokens.pop())


    def tokenize(self, s):
        t = [
            ('mr', r'Overhead, the geese flew \d+ miles east\.'),
            ('ml', r'Overhead, the geese flew \d+ miles west\.'),
            ('incr', r'He sold .*? sheep\.'),
            ('decr', r'They paid for their .*? mistakes\.'),
            ('pout', r'And Abraham spoke!'),
            ('pin', r'He listened when his wife spoke\.'),
            ('while', r'He ran into the mountains, but only when .*?\. This is what happened there\:'),
            ('loopend', r'Alas, I digress\.'),
            ('store', r'Preparing for the storm, he carved .*? into the stone\.'),
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
                self.has_error = True
                self.error = 'Problem with syntax in position %s' % m.start()
                return output

            if m.lastgroup in ['mr', 'ml', 'incr', 'decr']:
                output.append(m.lastgroup)
                output.append(self.processDigitToken(m))

            elif m.lastgroup == 'store':
                output.append(m.lastgroup)
                output.append(self.processStoreToken(m))

            elif m.lastgroup == 'while':
                output.append(m.lastgroup)
                output.extend(self.processCond(m))

            else:
                output.append(m.lastgroup)
            lastend = m.end()

        if lastend != len(s) and s[-1]!=' ':
            self.has_error = True
            self.error = 'Problem with syntax in position'

        output.reverse()

        return output


    def interpret(self, abraham_code, *args):
        self.buffer = [a for a in args]

        self.i = 0
        self.tape = [0]
        self.tokens = list()
        self.loopcons = list()
        self.loopactions = list()
        self.cval = 0
        self.output = ''

        self.tokens = self.tokenize(abraham_code)
        self.consumeTokenList()
        if self.has_error:
            return self.error
        else:
            return self.output

