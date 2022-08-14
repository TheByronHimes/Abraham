from abeinterpreter import AbeInterpreter

def test_move_right():
    ai = AbeInterpreter()
    ai._tokens.append('1')
    ai._mr()
    assert ai._i == 1


def test_illegal_move_left():
    ai = AbeInterpreter()
    ai._tokens.append('1')
    ai._ml()
    assert ai._error == 'Not allowed to move left of index 0.'


def test_move_left():
    ai = AbeInterpreter()
    ai._tokens.append('3')
    ai._mr()
    ai._tokens.append('2')
    ai._ml()
    assert ai._i == 1


def test_incr_1():
    ai = AbeInterpreter()
    ai._tokens.append('1')
    ai._incr()
    assert ai._tape[ai._i] == 1


def test_incr_7():
    ai = AbeInterpreter()
    ai._tokens.append('7')
    ai._incr()
    assert ai._tape[ai._i] == 7


def test_sequential_incr():
    ai = AbeInterpreter()
    ai._tokens.append('4')
    ai._incr()
    ai._tokens.append('3')
    ai._incr()
    assert ai._tape[ai._i] == 7


def test_decr_1():
    ai = AbeInterpreter()
    ai._tokens.append('1')
    ai._decr()
    assert ai._tape[ai._i] == -1


def test_decr_7():
    ai = AbeInterpreter()
    ai._tokens.append('7')
    ai._decr()
    assert ai._tape[ai._i] == -7


def test_sequential_decr():
    ai = AbeInterpreter()
    ai._tokens.append('4')
    ai._decr()
    ai._tokens.append('3')
    ai._decr()
    assert ai._tape[ai._i] == -7


def test_sequential_incr_decr():
    ai = AbeInterpreter()
    ai._tokens.append('8')
    ai._incr()
    ai._tokens.append('5')
    ai._decr()
    assert ai._tape[ai._i] == 3


def test_neg_incr():
    ai = AbeInterpreter()
    ai._tokens.append('-8')
    ai._incr()
    assert ai._tape[ai._i] == -8


def test_neg_decr():
    ai = AbeInterpreter()
    ai._tokens.append('-8')
    ai._decr()
    assert ai._tape[ai._i] == 8


# TODO: write tests for input function

def test_copy():
    ai = AbeInterpreter()
    ai._tape[ai._i] = 17
    ai._copyVal()
    assert ai._cval == 17


def test_paste():
    ai = AbeInterpreter()
    ai._cval = 17
    ai._pasteVal()
    assert ai._tape[ai._i] == 17


def test_copy_then_paste():
    ai = AbeInterpreter()
    ai._tape[ai._i] = 17
    ai._copyVal()
    ai._tokens.append('1')
    ai._mr()
    ai._pasteVal()
    assert ai._i == 1 and ai._tape[ai._i] == 17


def test_cast_int():
    ai = AbeInterpreter()
    x = ai._cast('int', '1')
    assert x == 1


def test_cast_float_to_int():
    ai = AbeInterpreter()
    x = ai._cast('int', '1.0')
    assert x is None and ai._error == 'Could not cast 1.0 to type int'


def test_cast_str_to_int():
    ai = AbeInterpreter()
    x = ai._cast('int', 'hello world')
    assert x is None and ai._error == 'Could not cast hello world to type int'


def test_cast_bool_to_int():
    ai = AbeInterpreter()
    x = ai._cast('int', 'True')
    assert x is None and ai._error == 'Could not cast True to type int'


def test_cast_float():
    ai = AbeInterpreter()
    x = ai._cast('float', '1.2')
    assert x == 1.2


def test_cast_int_to_float():
    ai = AbeInterpreter()
    x = ai._cast('float', '1')
    assert x == 1.0


def test_cast_str_float():
    ai = AbeInterpreter()
    x = ai._cast('float', 'hello world')
    assert x is None and ai._error == 'Could not cast hello world to type float'


def test_cast_bool_to_float():
    ai = AbeInterpreter()
    x = ai._cast('float', 'True')
    assert x is None and ai._error == 'Could not cast True to type float'


def test_cast_str():
    ai = AbeInterpreter()
    x = ai._cast('str', '1')
    assert x == '1'


def test_cast_bool_true():
    ai = AbeInterpreter()
    x = ai._cast('bool', 'True')
    assert x == True


def test_cast_bool_false():
    ai = AbeInterpreter()
    x = ai._cast('bool', 'False')
    assert x == False