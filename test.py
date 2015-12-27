#!/usr/bin/python
import sys 

def testLocalDisplay():
    import Tests.TestPygameDisplay as T1
    T1.main()

def testSocketUDP():
    import Tests.TestSocketsUDP as T2
    T2.main()

def testSimpleProtocol():
    import Tests.TestSimpleProtocol as T3
    T3.main()

def testSendData():
    import Tests.TestSendData as T4
    T4.main()

def main(argv):
    if len(argv)>0:
        if(argv[0]=="localDisplay"):
            testLocalDisplay()
        elif(argv[0]=="socketUDP"):
            testSocketUDP()
        elif(argv[0]=="simpleProtocol"):
            testSimpleProtocol()
        elif(argv[0]=="sendData"):
            testSendData()
        else:
            print("Test not valid")
    else:
        print("To run the tests, run ./test.py [command]")
        print("The list of commands can be found at the moment in the source of test.py")

if __name__ == "__main__":
   main(sys.argv[1:])


