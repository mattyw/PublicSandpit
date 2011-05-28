from multiprocessing import Process, Pipe
import optimus_requester
import time
addresses = {'machine1':'http://localhost:8989',
             'machine2': 'http://localhost:8989',
             'machine3':'http://localhost:8989'}


class ProcessManagement:
    def __init__(self, name, proc, pipe):
        self.name = name
        self.proc = proc
        self.pipe = pipe 


def main():
    proccess_managers = []
    for name in addresses.keys():
        parent_conn, child_conn = Pipe()
        p = Process(target=optimus_requester.make_process, args=(name, addresses[name], 0.5, child_conn))
        proccess_managers.append(ProcessManagement(name, p, parent_conn))
        parent_conn.send(1)
        p.start()
        time.sleep(0.5) #Pause between starting processes
    
    while True:
        alive = 0
        dead = 0
        for manager in proccess_managers:
            if manager.proc.is_alive():
                alive += 1
            else:
                dead += 1
            manager.pipe.send(1)
        print '%s of %s processes still running' %(alive, len(proccess_managers))
        time.sleep(1)
if __name__ == '__main__':
    main()