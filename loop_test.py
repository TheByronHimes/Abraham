from abeinterpreter import AbeInterpreter


def test_bad_loop_condition():
    ai = AbeInterpreter()
    out = ai.interpret('He ran into the mountains, but only when he had less than 10 fish. This is what happened there:')
    assert out == 'Loop condition syntax is incorrect.'


def test_simple_dec_loop():
    ai = AbeInterpreter()
    out = ai.interpret('He sold 5 sheep. He ran into the mountains, but only when they had more than 1 fish. This is what happened there: They paid for their 1 mistakes. Alas, I digress. And Abraham spoke!')
    out = out.rstrip('\n')
    assert out == '1'


def test_simple_inc_loop():
    ai = AbeInterpreter()
    out = ai.interpret('He ran into the mountains, but only when they had less than 10 fish. This is what happened there: He sold 1 sheep. Alas, I digress. And Abraham spoke!')
    out = out.rstrip('\n')
    assert out == '10'


def test_nested_loop():
    ai = AbeInterpreter()
    out = ai.interpret('''He sold 2 sheep. 
                        He ran into the mountains, but only when they had more than 0 fish. This is what happened there: 
                        They paid for their 1 mistakes. Overhead, the geese flew 1 miles east. He sold 2 sheep. 
                        He ran into the mountains, but only when they had more than 0 fish. This is what happened there: 
                        They paid for their 1 mistakes. Overhead, the geese flew 1 miles east. He sold 1 sheep. Overhead, the geese flew 1 miles west. 
                        Alas, I digress. 
                        Overhead, the geese flew 1 miles west.
                        Alas, I digress. 
                        Overhead, the geese flew 2 miles east. 
                        And Abraham spoke!''')

    out = out.strip('\n')
    assert out == '4'
