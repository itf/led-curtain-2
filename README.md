Getting started with Iron Curtain 2 development. 

![screenshot](https://raw.githubusercontent.com/Donlanes/iron-curtain-2/master/docs/cloudsRainbow.png)
![screenshot](https://raw.githubusercontent.com/Donlanes/iron-curtain-2/master/docs/mesmerizingMeteor.png)
![screenshot](https://raw.githubusercontent.com/Donlanes/iron-curtain-2/master/docs/rainbowAurora.png)

##Quick Start

* Install pygame
* Install pypy (Or download it to the same directory and run it)
* Run: python LocalDisplay.py 
* Run: pypy Cli.py

Using images:
* install pillow on pypy:
* First way:
	* Download https://github.com/python-pillow/Pillow
	* Run: pypy setup.py install from that directory
* Second way:
	* Install pip in pypy :
	*  Download pip from [wget] https://bootstrap.pypa.io/get-pip.py 
	* [sudo]  pypy get-pip.py
	* [sudo] pypy -m pip install pillow
Change Images to True in config.py

Using Audio:
Making the audio work is non-trivial. If you still want to do so, follow the following instructions!
* Install jack
	* Instaling jack is hard. That is a fact. So try this step before the others.
	* To install on windows, read here http://jackaudio.org/faq/jack_on_windows.html	
	* To install on ubuntu, install jack2 and then pulseaudio-module-jack and reset.
	* TO install on Mac, good luck.
* install pyjack on cpython (sudo python -m pip install pyjack /  pip install pyjack / download pyjack and run setup.py
* install a jack patchbay. I recommend kxstudio Cadence/Claudia  for Ubuntu or Windows
	* It is easier to simply use a patchbay to redirect output than to do it programatically, when writting crossplatform code
* Install Numpy. 
	* pip install numpy should do. Otherwise http://docs.scipy.org/doc/numpy-1.10.1/user/install.html
* Install aubio  https://aubio.org/download
* Install python bindings for aubio
	* Download https://github.com/aubio/aubio/tree/master/python
	* run [python] setup.py install
* Change Audio to True in config.py

* Start the audio server. 
	* Run: AudioServer.py
* Run your jack patchbay and connect the output from jack sink to the ledaudio node
* Use 'beat' on your patterns

##Cli pattern programming language

The Command Line interface has its own programming language to combine patterns. 

Pressing <b>TAB</b> twice on the CLI will suggest code completion. Functions differ from patterns by the presence of the parenthesis. 

Pressing  <b>TAB</b>  inside args will suggest args for your pattern

<b>Always press TAB</b>  to autocomplete your patterns and get suggestion for parameters.

The only argument that functions take are patterns, with the exception of the function args  (and, until the moment, function UpdateRate, FrameRate and TimeChanger, which are still being adapted to the new syntax)

The easiest way to learn how to use the CLI is by examples. Example of patterns on the CLI:

To modify the parameters of the functions use the function arg('')(

To modify the parameters without using arg, write r to set the values of the parameters once, or rr to modify the values continuosly

* red ->  outputs a red pattern
* rainbownize(red) ->  horizontally HUE shifts red to turn it into a rainbow
* vRainbowinize(rainbownize(red)) ->  Diagonal Rainbows	

* trivial ->  repeats its input, i.e. ouputs the previous canvas.
* blur(trivial) ->  blurs the previous output
* step(rainbow, blur(trivial) ) -> initializes a rainbow, and then starts blurring it
* step(random, gameOfLife(trivial)) -> intializes a random canvas and then run gameOfLife on top of it

* movingHue(red) -> changing colors
* movinHue(rainbow) -> moving rainbow
* movingHue(constant(random))  -> initializes a random canvas, saves this canvas, and applies a frame dependent hue change on it.

* meanP(red,blue) -> takes the mean of red and blue
* movingHue(meanP(movingColors,rainbow))  -> softRainbow

* mask(circle, blue, green) -> masks a blue circle on top  of green

* arg('cRadius=abs(frame%20-10)/30.')(circle)  -> pulsatingCircle
* arg('nRainbows=2')(rainbownize(red))  -> doubleRainbow

* arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2')(mask(translate(circle),meanP(softRainbow,trivial),blur(trivial))) 
					-> moving masked circle with blurring background
* hueShift(arg('xTranslate= cos(frame/37.); yTranslate = sin(frame/60.)*2; weightedMeanWeight=0.03; hue=0.021')(mask(translate(circle),prettyDiagonalRainbow, weightedMean2P(black,blur(trivial)))))) 
					-> movingCircle with fading to black background (_mesmerezingMeteor)


* arg('generationBornRange=[3,4]; generationSurviveRange=[1,2,3]; generationStates=48; generationNeighborDistance=1 ')(isolate(step(circle,gameOfGeneration(trivial)))))
			-> Super cool pattern. Runs isolated, i.e.  doesn't interact with outside args nor canvas

* r hue=0.5  -> sets hue to 0.5
* hueShift(red)  -> now red is shifted by 0.5

* rr hue= abs(sin(frame/30.))  -> evaluates this function in every update, and updates the hue
* hueShift(red)  -> now red is shifted by a variable amount
* rr -> evaluates nothing on every update.Erases previous RR instruction

* s -> saves the pattern
* ss ->safe saves the pattern, i.e. saves the pattern with an isolate canvas. Useful if the pattern makes use of trivial.

##Debian Install
* For fake display.
sudo apt-get install python-pygame



For testing, you are still using UDP sockets. They are pretty computation intensive, but this is to assure that the code would run with the led panel


It has autocomplete for the functions and patterns

##Improving performance
Function calls are pretty expensive when using the python compiler.  Instead of using the default compiler, use pypy

http://pypy.org/download.html

for Debian:

apt-get install pypy

example:

pypy Cli.py

This will make the code 2 to 4 times more efficient for simple functions, and can give a N times performance improvement where N is the number of nested functions, apparently, for more complex code.


##Troubleshooting
CLI should run out of box with no problemon linux and mac

If you use windows you will need the readline module.

There are two ways of getting the readline module: install it or run inside pypy. Installing pypy is the preferred method, since it improves performance.

If you want to install the module and run it in python, install it from here: https://pypi.python.org/pypi/readline	



##TODO
[x]Integrate audio

[]separate functions that are inside patterns to a separate file and organize them

[x]Write saver and importer

[]Standardize the input to functions

[x]Decorator to make functions that take patternInputs and extra parameters  take patterns and extra parameters

[] list function list the name of the input variables to functions.

[] Find a way to make it clear that certain functions take arguments

[] split CLI in multiple files

[x] Mock audio processing

[x] Implement lazy evaluation for canvas

[x] Find the problems with pretty diagonal rainbow. Possible meta function problem?

[] Improve parameter input in CLI  http://ironalbatross.net/wiki/index.php?title=Python_Readline_Completions

[x] Improve compose performance (implent it in log n instead of N)

[x] make function or meta function  F(arg)(function that takes pattern Input and changes arg). Need special syntax for that 
function -> http://stackoverflow.com/questions/13923091/how-do-you-do-a-python-eval-only-within-an-object-context + eval

[x] implement Isolate in a better way

[] frame update / audio update done outside the ui, so it can be called from isolate

[] add previous pattern to pattern input

[] add code to run on a raspberry pi, communicating with the LED strips

[] create save with arguments and default arguments

[] make it possible to save functions.