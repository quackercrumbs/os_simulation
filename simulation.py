from memory_manager import *
from disk_manager import *
from printer_manager import *
from process import *
from processor import *
from scheduler import *
from utils import Util
import re


mem_size = 0
num_hdd = 0
num_printer = 0

#get user input
print("How much RAM Memory is there on the simulated computer?")
mem_size = int(input('>'))
while(mem_size <= 0):
    print("Please print a valid size.")
    mem_size = int(input('>'))

print("How many hard disks the simulated computer has?")
num_hdd = int(input('>'))
while(num_hdd <= 0):
    print("Please print a valid size.")
    mem_size = int(input('>'))


print("How many printers the simulated computer has?")
num_printer = int(input('>'))
while(num_printer <= 0):
    print("Please print a valid size.")
    mem_size = int(input('>'))

print('Your simulated computer has {} bytes of RAM,  {} HDD(s),  {} Printer(s).'.format(mem_size, num_hdd, num_printer))

#computer components
cpu = CPU()
sched = Scheduler()
mem_manager = MemoryManager(mem_size)
hd_manager = HardDriveManager(num_hdd)
printer_manager = PrinterManager(num_printer)
utils = Util()

user_input = ''

#wait for input
while(True):
    print("What would you like to do?")
    user_input = input('>')
    #verify inputs
    while(not utils.isValid(user_input)):
        print("Enter valid command!")
        user_input = input('>')
    #do command
    if(utils.new_process.match(user_input)):
        #parse the input, retrieve the priority and size, and create the new process
        variables = re.split('\W+',user_input)
        #create process and pcb
        p = Process(int(variables[1]), int(variables[2]))
        success = mem_manager.put(p)
        if(not success):
            print('No room in memory.')
            break

        if(sched.peek_highest() == -1 and not cpu.isBusy()):
            #there are no schedule processes and cpu is free
            cpu.run(p)
        elif(cpu.check_priority() < p.priority):
            #prempt cpu and allow higher prioty process into cpu
            print('Preempted')
            temp = cpu.terminate()
            cpu.run(p)
            #put back into queue
            sched.put(temp)
        else:
            print('Goes to the ready queue!')
            sched.put(p)
        
    if(utils.terminate.match(user_input)):
        #terminate the process
        t = cpu.terminate()
        #free the memory space taken
        mem_manager.release(t)
        #put next item into cpu
        p = sched.get()
        if(p != None):
            cpu.run(p)
        else:
            print("No processes running.")
    if(utils.disk_request.match(user_input)):
        variables = re.split('\W+',user_input)
        if(not utils.inRange(hd_manager.size,int(variables[1]))):
            print('Disk {} does not exist.'.format(int(variables[1])))
            continue
        t = cpu.terminate()
        if(t == None):
            print('There is no process in the cpu.')
            continue
        hd_manager.put(int(variables[1]),t)
        p = sched.get()
        if( p != None):
            print('New process running in CPU.')
            cpu.run(p)
        else:
            print('CPU is now empty.')
    if(utils.disk_complete.match(user_input)):
        variables = re.split('\W+',user_input)
        if(not utils.inRange(hd_manager.size,int(variables[1]))):
            print('Disk {} does not exist.'.format(int(variables[1])))
            continue
        p = hd_manager.complete(int(variables[1]))
        if(p == None):
            print('There are no processes in hard drive {}'.format(variables[1]))
            continue
        if(sched.peek_highest() == -1 and not cpu.isBusy()):
            print(p)
            cpu.run(p)
        elif(cpu.check_priority() < p.priority):
            print('Preempted')
            temp = cpu.terminate()
            cpu.run(p)
            sched.put(temp)
        else:
            print('Goes to the ready queue!')
            sched.put(p)
    if(utils.print_request.match(user_input)):
        variables = re.split('\W+',user_input)
        if(not utils.inRange(printer_manager.size,int(variables[1]))):
            print('Printer {} does not exist.'.format(int(variables[1])))
            continue
        t = cpu.terminate()
        if(t == None):
            print('There is no process in the cpu.')
            continue
        printer_manager.put(int(variables[1]),t)
        p = sched.get()
        if( p != None):
            print('New process running in CPU.')
            cpu.run(p)
        else:
            print('CPU is now empty.')
    if(utils.print_complete.match(user_input)):
        variables = re.split('\W+',user_input)
        if(not utils.inRange(printer_manager.size,int(variables[1]))):
            print('Printer {} does not exist.'.format(int(variables[1])))
            continue
        p = printer_manager.complete(int(variables[1]))
        if(p == None):
            print('There are no processes in Printer {}'.format(variables[1]))
            continue
        if(sched.peek_highest() == -1 and not cpu.isBusy()):
            print(p)
            cpu.run(p)
        elif(cpu.check_priority() < p.priority):
            print('Preempted')
            temp = cpu.terminate()
            cpu.run(p)
            sched.put(temp)
        else:
            print('Goes to the ready queue!')
            sched.put(p)
    if(utils.show_ready.match(user_input)):
        cpu.snapshot()
        sched.snapshot()
    if(utils.show_io_ready.match(user_input)):
        printer_manager.snapshot()
        hd_manager.snapshot()
    if(utils.show_memory.match(user_input)):
        mem_manager.snapshot()


