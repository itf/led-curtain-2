curtain = "old"

if curtain=="old":
    width = 15
    height = 5
    host='10.0.63.101'
    port=6038
    import Transportation.Protocol.OldProtocol as P
    Protocol = P
else: #Assume local
    width = 60
    height = 30
    host='localhost'
    port=5000
    import Transportation.Protocol.SimpleProtocol as P
    Protocol = P
