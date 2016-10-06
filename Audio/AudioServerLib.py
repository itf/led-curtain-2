import numpy
import jack
import time
from aubio import tempo, source
import Transportation.Sockets.ClientSocketUDP as Client
from Config import AudioServerConfig as Config

DEBUG = 1

def rollAndAverage(arr, rolls):
    for roll in rolls:
        aux =  (arr + numpy.roll(arr, roll))/2
        del arr
        arr =aux
    return arr

def audioProcess(port, host='localhost'):
    try:
        jack.attach("ledaudio")

        print (jack.get_ports())

        jack.register_port("in_1", jack.IsInput)

        jack.activate()

        print (jack.get_ports())

        jack.connect("system:capture_1", "ledaudio:in_1")

        print (jack.get_connections("ledaudio:in_1"))

        N = jack.get_buffer_size()
        Sr = float(jack.get_sample_rate())
        print ("Buffer Size:", N, "Sample Rate:", Sr)

        capture = numpy.zeros((1,N), 'f')
        output = numpy.zeros((1,N), 'f')

        print ("Capturing audio...")

        i = 0
        win_s = 1024                # fft size
        hop_s =  win_s/8          # hop size
        o = tempo("default", win_s, hop_s, int(Sr))

        clientSocket = Client.ClientSocketUDP(host,port)
        audioIntensityBuffer = numpy.zeros((1,2*N), 'f')

        while 1:
            try:
                jack.process(output, capture[:,0:0+N])
                audioIntensityBuffer[0,0:N] = capture
                audioIntensityBuffer = numpy.roll(audioIntensityBuffer,-N)
                intensity = numpy.square(audioIntensityBuffer).mean()
                lowFreqIntensity = numpy.square(rollAndAverage(audioIntensityBuffer,[1,4,8,16])).mean()
                clientSocket.sendData("I#"+str(intensity))
                clientSocket.sendData("L#"+str(lowFreqIntensity))
                #audioMono = 
                for i in xrange(1,int(N/hop_s)+1):
                    if o(capture[0,(i-1)*hop_s:i*hop_s]):
                        clientSocket.sendData("beat")
                        if DEBUG:
                            print ("beat")
                i += N
            except jack.InputSyncError:
                print ("Input Sync")
                pass
            except jack.OutputSyncError:
                print ("Output Sync")
                pass
            if DEBUG == 2:
                print ('.',)

    except KeyboardInterrupt:
        try:
            jack.deactivate()
        except:
            pass
        try:
            jack.detach()
        except:
            pass

