# Abraham
Esoteric language interpreter

**************************************
Install:
--------
pip install abeinterpreter

**************************************

Basic Usage:
------------
0. Import:
	<code>import abeinterpreter as ai</code>

1. Instantiate the AbeInterpreter class:
	<code>interp = ai.AbeInterpreter()</code>

2. Interpret code with .interpret(code):
	<code>interp.interpret(*some abe code here*)</code>

3. Display output with print:
	<code>print(interp.interpret(*some abe code here*))</code>

**************************************
Types:	
------
<ul>
<li>String: "Hello World!"</li>
<li>Int: 42</li>
<li>Float: 3.14</li>
<li>Boolean: True, False</li>
</ul>

**************************************
Commands:
---------
<ul>
<li>Move right x cells:	Overhead, the geese flew x miles east.</li>
<li>Move left x cells:	Overhead, the geese flew x miles west.</li>
<li>Assign x to cell:	Preparing for the storm, he inscribed x into the stone.</li>
<li>Add to cell value:	He sold x sheep.</li>
<li>Subtract from cell value:	They paid for their x mistakes.</li>
<li>Print cell value:	And Abraham spoke!</li>
<li>While loop:	He ran into the mountains, but only when ___. This is what happened there:</li>
<li>Note:	Loop conditions act on current cell value.</li>
<li>Loop conditions:	If greater than cell val: they had more than x fish</li>
<li>If less than cell val: they had less than x fish</li>
<li>If equal to cell val: the stone said x</li>
<li>Signal loop end:	Alas, I digress.</li>
<li>Copy:	One day he stole his neighbor's goods.</li>
<li>Paste:	He repented and returned the property.</li>
</ul>

**************************************
Print even integers from 100 to zero:	
-------------------------------------
<code>He sold 100 sheep. 
He ran into the mountains, but only when they had more than 0 fish. 
This is what happened there: 
And Abraham spoke! 
They paid for their 2 mistakes. 
Alas, I digress. 
And Abraham spoke!</code>

**************************************
