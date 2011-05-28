import xmlrpclib
from datetime import datetime
import time
class OptimusRequester():
    def __init__(self, name, address):
        pass
        
    def send_request(self):
            print 'doing stuff'
                
    def do_request_loop(self, sleep_seconds, conn):
        while True:
            self.send_request()
            time.sleep(sleep_seconds)
            conn.poll()
            
def make_process(name, address, sleep_seconds, conn):
    r = OptimusRequester(name, address)
    while True:
        r.send_request()
        time.sleep(sleep_seconds)
        if conn.poll(5):
            conn.recv()
        else:
            break
            
    

if __name__ == '__main__':
    
    o = OptimusRequester('machine1', 'http://localhost:2001')
    while True:
        o.send_request()
    
#    m1 = MachineState('m1', 'f')
#    m2 = MachineState('m2', 'ff')
#    m3 = MachineState('m3', 'fff')
#
#    o.add_or_update(m1)
#    o.add_or_update(m2)
#    o.add_or_update(m3)
