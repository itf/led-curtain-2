import numpy
import jack
import time
from aubio import tempo, source
import Transportation.Sockets.ClientSocketUDP as Client
from Config import AudioServerConfig as Config

DEBUG = 0

def audioProcess(port, host='localhost'):
    try:
        jack.attach("ledaudio")

        print jack.get_ports()

        jack.register_port("in_1", jack.IsInput)

        jack.activate()

        print jack.get_ports()

        jack.connect("system:capture_1", "ledaudio:in_1")

        print jack.get_connections("ledaudio:in_1")

        N = jack.get_buffer_size()
        Sr = float(jack.get_sample_rate())
        print "Buffer Size:", N, "Sample Rate:", Sr

        capture = numpy.zeros((1,N), 'f')
        output = numpy.zeros((1,N), 'f')

        print "Capturing audio..."

        i = 0
        win_s = 1024                # fft size
        hop_s =  win_s/8          # hop size
        o = tempo("default", win_s, hop_s, int(Sr))

        clientSocket = Client.ClientSocketUDP(host,port)

        while 1:
            try:
                jack.process(output, capture[:,0:0+N])
                #audioMono = 
                for i in xrange(1,int(N/hop_s)+1):
                    if o(capture[0,0:i*hop_s]):
                        clientSocket.sendData("beat")
                        if DEBUG:
                            print ("beat")
                i += N
            except jack.InputSyncError:
                print "Input Sync"
                pass
            except jack.OutputSyncError:
                print "Output Sync"
                pass
            if DEBUG == 2:
                print '.',

    except KeyboardInterrupt:
        try:
            jack.deactivate()
        except:
            pass
        try:
            jack.detach()
        except:
            pass

