LED Matrix pattern generator and controller

![screenshot](https://raw.githubusercontent.com/Donlanes/iron-curtain-2/master/docs/cloudsRainbow.png)
![screenshot](https://raw.githubusercontent.com/Donlanes/iron-curtain-2/master/docs/mesmerizingMeteor.png)
![screenshot](https://raw.githubusercontent.com/Donlanes/iron-curtain-2/master/docs/rainbowAurora.png)

Demo of an earlier version of the code (the lag and statering was caused by sending the data over wifi, which was not reliable. Sending the data over etherned fixes the problem).
https://www.youtube.com/watch?v=TaUksNn31NY


##Quick Start UNIX

* Install pygame, if you want to develop locally
* Install pypy (Or download it to the same directory and run it)
* Run: python LocalDisplay.py 
* Copy Config.py to LocalConfig.py, and modify it.
* Run: pypy Cli.py
* Ctrl-c to close

Everything is run from the terminal

###Debian/Ubuntu Install

* sudo apt-get install pypy
*  * For local display.
*sudo apt-get install python-pygame


##Quick Start Windows

If you are on windows you will have to run everything under cpython and there will be a performance problem:
* Install pyReadline https://pypi.python.org/pypi/pyreadline
* Install pygame, if you want to develop locally
* Run: python LocalDisplay.py 
* Copy Config.py to LocalConfig.py, and modify it.
* Run: python Cli.py
* Ctrl-c to close

Everything is run from the command line

###Using images:

* install pillow on pypy (or cPython):
(dependencies: sudo apt-get install pypy-dev python-dev)
* First way:
	* Download https://github.com/python-pillow/Pillow
	* Run: pypy setup.py install from that directory
	* Or for python: python setup.py install from that directory
* Second way:
	* Install pip in pypy :
	*  Download pip from [wget] https://bootstrap.pypa.io/get-pip.py 
	* [sudo]  pypy get-pip.py
	* [sudo] pypy -m pip install pillow
	* Or, for python, pip install pillow

And then change Images to True in config.py

### Screen Capture

On Windows and OSX, simply install pillow. For Linux, install pyscreenshot. pypy -m pip install pyscreenshot.

### Husl

A different color space. Can make some nice colors for patterns. Install husl: sudo pypy -m pip install husl

### Using Weather

Install requests (sudo pypy -m install requests)
Create an account on openweather, and configure your city ID and your API Key in local config

###Using Audio:

Making the audio work is non-trivial. If you still want to do so, follow the following instructions!
* Install jack
	* Instaling jack is hard. That is a fact. So try this step before the others.
	* To install on windows, read here http://jackaudio.org/faq/jack_on_windows.html
	* To install on ubuntu, install jack2 and then pulseaudio-module-jack and reset.
	* TO install on Mac, good luck.
* install pyjack on cpython (sudo python -m pip install pyjack /  pip install pyjack / download pyjack and run setup.py)
* DO NOT INSTALL JACK.py (pip intall jack), because it is incompatible with pyjack
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
* Use 'beat' or 'totalBeats' on your patterns


#Installing on the raspberry pi to control
I use the python bindings for rpi_ws281x; however, I had to modify the code to improve its performance. Check it out on
https://github.com/itf/rpi_ws281x.
You will need to install, swig and python-dev to compile it.

Instructions: install scons, install swig, install python-dev. Go to the top directory, run sudo scons. Cd into the python directory and run sudo python setup.py install

Also, remember to run piUdpBuffer.sh, to remove lag caused by the UDP buffer

#Cli pattern programming language - Quick start

The Command Line interface has its own programming language to combine patterns. 

Pressing <b>TAB</b> twice on the CLI will suggest code completion. Functions differ from patterns by the presence of the parenthesis. 

Pressing  <b>TAB</b>  inside args will suggest args for your pattern

<b>Always press TAB</b>  to autocomplete your patterns and get suggestion for parameters.

The syntax of this short programming language is the same as python. Every function takes as arguments one or more patterns, with exception of the function "arg". Example addP(red,green) becomes yellow. In order to modify the behavior.

In order to modfy the parameters that a function or pattern depend on, you should use the function arg('arguments=something')(function(pattern)). So to set the radius of a circle to be the same as the height of your led panel, do:

arg('circleRadius=1')(circle)


To modify the parameters without using arg, write r to set the values of the parameters once, or rr to modify the values continuosly


The easiest way to learn how to use the CLI is by examples. Example of patterns on the CLI:


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

* arg('circleRadius=abs(frame%20-10)/30.')(circle)  -> pulsatingCircle
* arg('nRainbows=2')(rainbownize(red))  -> doubleRainbow

* arg('translateX= cos(frame/37.); translateY = sin(frame/60.)*2')(mask(translate(circle),meanP(softRainbow,trivial),blur(trivial))) 
					-> moving masked circle with blurring background
* hueShift(arg('translateX= cos(frame/37.); translateY = sin(frame/60.)*2; weightedMeanWeight=0.03; hue=0.021')(mask(translate(circle),_prettyDiagonalRainbow, weightedMean2P(black,blur(trivial))))))
					-> movingCircle with fading to black background (_mesmerezingMeteor)


* arg('generationBornRange=[3,4]; generationSurviveRange=[1,2,3]; generationStates=48; generationNeighborDistance=1 ')(isolate(step(circle,gameOfGeneration(trivial)))))
			-> Super cool pattern. Runs isolated, i.e.  doesn't interact with outside args nor canvas

* r hue=0.5  -> sets hue to 0.5
* hueShift(red)  -> now red is shifted by 0.5

* rr hue= abs(sin(frame/30.))  -> evaluates this function in every update, and updates the hue
* hueShift(red)  -> now red is shifted by a variable amount
* rr -> evaluates nothing on every update.Erases previous RR instruction

####Saving
* s -> saves the pattern
* ss ->safe saves the pattern, i.e. saves the pattern with an isolated canvas. Useful if the pattern makes use of trivial.
* srr-> saves with the rr arguments you were using.


####Audio example:

* hueShift(circle
* rr circleRadius=beat; hue = int(totalBeats%4)/4.
* srr
* name of this pattern


#Project Detail

##Objective

This projects was created with the objective of controlling a 30x60 Ws2812b led panel. The objectives of the sofware part of the code were:

* Be capable of creating new functions by combining previous ones (Functional programming style).
* Mostly, if not all, in a single language
* Run on Linux, Windows and Mac
* Be able to react to music / beats
* Have few dependencies / dependencies that are easy to install
* Be modular (Easy to add new protocols, new functions, patterns, etc)
* Communicate through UDP over ethernet/wifi to send the data.
* Be easy for people with little experience with programming to contribute to the project.

This code was never meant to be efficient, and would probably struggle controlling anything larger than 100x100 pixels unless it was partially rewritten to make use of C extensions. Running the code under pypy is necessary if you want to do lots of hue operations, since function calls in pypy are much more efficient than in Cpython.

##Code organization

There are 3 main types of executables in the code. The pattern generator, the display manager, and the audio listener. 

The pattern generator runs the patterns and sends the resulting data through UDP to the display.

The display manager listens for data from the pattern generator and sends the data to the display.

The audio listener processes audio events and sends data through UDP to the pattern generator.

###Display manager

The display manager code is really simple: it is a while loop that reads data from a UDP socket and forwards it to the real display. There are two display managers in the code: LocalDisplay and PiDisplay. The first is used to control a local display on your own computer; useful when testing code. The second is used by a raspberry pi to send data to Ws2812b strips.

###Audio Listener

The audio listener is also really simple: it uses the 'jack' python code, in order to have access to the audio beeing played by the computer; uses a third party library to perform beat detection and sends this data through UDP to a port specified on the Config file.

###Pattern Generator

This is where all the magic happens. It is made by the UI, audio event listener, canvas, patternInput, patterns, functions, color manager, savedFunctions and savedPatterns.

####UI

At the moment, the UI is responsible for getting input from the user, run the patterns, update the frame count eveyrtime a pattern is run, restart the frame count when the pattern being run changes, initialize the audio event listener, create the initial patternInput, add the audio functions to the pattern input and adds the previousPattern to the patternInput.

Ideally it should be split in multiple modules, but there was a lack of time.

At the moment there is a single user interface, called CLI, which stands for Comman Line Interface. The CLI runs in the command line, or terminal, and makes use of the pyreadline for code completion. It has its own short programming language, that was described previously on this Readme.

####Audio Event Listener

The audio event listener keeps track of the BPM, Total Beats, and where in the beat you are.

Every time it receives a new beat event, it updates its BPM. 

The Beat is a value between 0 and 1 that describes where in the beat you are. At 0, a beat has just happened. At 1, it is about to happen. At 0.5 it is half away between the beats.   The beat value can never decrease by less than 0.5 between calls of the beat function, in order to make sure that patterns won't run backwards.

The TotalBeats, it is the same as Beats, but it is strictly increasing. TotalBeasts = Beat + total beats that happened so far.

####Canvas

The canvas is one of the few optimized places of the code. It is a representation of the color of each pixel on the display.

The important functions implemented by the canvas are:

* mapFunction : applies a function to every pixel of the canvas. It is implemented to be efficient and to use lazy evaluation.
* translateAndScale and restoreTranslateAndScale: allows running a pattern in a small portion of the canvas; to allow different patterns sharing the same display at the same time.
* __getitem__ : allows to access data from the Canvas as if it was a python array
* __setitem__ : alloes to set data on the Canvas as if it was a python array

####PatternInput

The patternInput is the input given to the patterns. It is a dictionary that contains the canvas, all the parameters necessary to evaluate the patterns and functions, and contains the audio functions.

Instead of returning a function when accessing a function inside the patternInput, it returs the evaluation of the function, which allow patterns to use the audioFunctions (Beat, totalbeats) as if they were numbers.

Initially, the patternInput is almost empty, but after running patterns it gets populated with their arguments. Example: after running "circle" patternInput is populated with circleRadius, which can be modified to change the radius of the circle.

If something is not present on the patternInput, it is evaluated to 0, which provides some extra protection against patterns that could potentially depend on a pattern having run before them.

####Pattern

Patterns are functions that take a patternInput and return a modified patternInput. 

Usually the patterns modify the canvas inside the patternInput, so that they can display something on the display.

You can take a look at some of the patterns by accessing Patterns/StaticPatterns/basicPatterns

####Functions

Functions are functions (derp) that take one or more patterns and modify them. One example of function is 'hueShift', which shifts the hue of every pixel on the patternInput returned by a pattern.  Other examples are 'meanP', which takes the mean of one or more patterns; 'isolateCanvas' which protects the canvas that runs inside a pattern from being modified outside it; 'arg' which modifies the parameters inside the patternInput before running the pattern; 'transitionFade' which transitions smoothly from the previous pattern to the new pattern.

Functions make extensive use of python @decorators, which allows the functions code to be very modular. Decorators are python functions that modify other functions. If you wish to contribute to the code, it is not necessary to understand exactly what they do, as long as you follow the examples in the code.

####Color Manager

As you might be aware, our eyes perceive lights in a logarithmic way. This is taken into account by you computer screen, which displays colors in the SRGB color space; which basically applies a log scale on the intensity of the colors before displaying them to you.

LEDs work in a linear color scale, rather than on the SRGB color scale. The color manager is responsible for converting between those two color spaces before sending the data to the display.

####Saved Functions and Saved Patterns

The user can create and save new functions and new patterns from the UI. They are saved as python code inside this python file.



##Testing design choices:

For testing, you are still using UDP sockets. They are more computation intensive than necessary when running the code locally, but this is to assure that the code would run with the led panel



##Performance

As said earlier, performance was not one of the main worries of this project. If you need to increase the performance of the code you should run the patternGenerator code from inside pypy.

Function calls are pretty expensive when using the python compiler.  

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

[x]separate functions that are inside patterns to a separate file and organize them

[x]Write saver and importer

[x]Standardize the input to functions

[x]Decorator to make functions that take patternInputs and extra parameters  take patterns and extra parameters

[] list function list the name of the input variables to functions.

[NOT] Find a way to make it clear that certain functions take arguments

[x] split CLI in multiple files

[x] Mock audio processing

[x] Implement lazy evaluation for canvas

[x] Find the problems with pretty diagonal rainbow. Possible meta function problem?

[] Improve parameter input in CLI  http://ironalbatross.net/wiki/index.php?title=Python_Readline_Completions

[x] Improve compose performance (implent it in log n instead of N)

[x] make function or meta function  F(arg)(function that takes pattern Input and changes arg). Need special syntax for that 
function -> http://stackoverflow.com/questions/13923091/how-do-you-do-a-python-eval-only-within-an-object-context + eval

[x] implement Isolate in a better way

[] frame update done outside the UI, so it can be called from isolate

[x]  audio update done outside the ui

[x] add previous pattern to pattern input to implement nice transitions

[x] add code to run on a raspberry pi, communicating with the LED strips

[x] create save with arguments

[] create save with  default arguments

[x] make it possible to save functions.

[x] Abstract the cli file to allow the creatipn of other UIs

[x] Equation Plotter 

[] Test Equation Plotter 3d and fix bugs on it

[x] Remove empty spaces when saving

[x] Scale function

[x] Brightness function

[] Pixel Art pattern

[x] Snake or something similar, function

[] Create Preview and a Gui

[] Tap for beat when not using audio

[] h functionName -> display the docs of the function to the user on the CLI

[] Easy way to create patterns that contain an internal state [probably following the example of transition functions]

[] Improve the Readme, explaining everything that the project does, and explaining the design choices.

[]Make arguments dependent on x and y

[x]Keep arguments that are modified inside args stay modified inside args. Create a function in pattern input called getDifference, which returns a dict. 

[x]Allow string arguments (arguments that use "getVal") to depend on themselves, such as : rgbB = "rgbB + cos(frame)". Assumes string arguments that are supposed to be strings, such as "text" don't use "getVal", but, rather, maybe other function. For this, create a copy of the pattern input dict with no string arguments. Modify "set" as well, to only set values if they are not strings.

