import queue

class Scheduler(object):

    def __init__(self):
        self.priority_map = [queue.Queue() for i in range(5)]

    #return highest level that is ready, -1 if empty
    def peek_highest(self):
        for i in range(5)[::-1]:
            if(not self.priority_map[i].empty()):
                return i
        return -1;

    #return the highest priority process and dequeue
    def get(self):
        highest = -1
        for i in range(5)[::-1]:
            if(not self.priority_map[i].empty()):
                highest = i
                break
        
        #there are no processes ready    
        if(highest == -1):
            return None

        return self.priority_map[highest].get()


    #insert process into queue
    def put(self, process):
        self.priority_map[process.priority].put(process)


    def snapshot(self):
        for i in range(5)[::-1]:
            t = self.stringify_for_p(i)
            print('Priority {}: {} '.format(i, t))

    def stringify_for_p(self, p):
        temp = []
        result = ''
        while(not self.priority_map[p].empty()):
            x = self.priority_map[p].get()
            if(x is None):
                break
            temp.append(x)
            result = result + '  ' + str(x.id)
        for i in range(len(temp)):
            self.priority_map[p].put(temp[i])
        return result

