# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:01:43 2017

@author: infinte1
"""
import heapq
import numpy as np
import matplotlib.pyplot as plt

# Waiting time is the sum of the periods spent waiting in the ready queue.
 
#####################################
#Data Structures and Algorithms Used#
#####################################
     # list(): similar to linked lists in c++ and java
     # heapq(): allows to perform Priority Queue operations on the list() using
     #          heap sort
     #dict(): Dictionary (Hash Table or Map)

def avgWaitingTime(waitingTimes):
    s= 0.0
    for v in waitingTimes.values():
        s += v
    l = len(waitingTimes.keys())
    avg = s/(l*1.0)
    return avg
    
        
    
def FCFS(n, burstTime,arrival):    
    begin = [None]*n
    end = [None]*n
    waiting = [None]*n
    waiting[0] = 0
    begin[0]=0
    end[0] = burstTime[0]    
    for i in range(1,n):
        begin[i] = end[i-1]
        end[i] = begin[i] + burstTime[i]
        waiting[i] = begin[i] - arrival[i]
    waitingTime = np.average(waiting) 
    times = list()
    for i in range(0,len(begin)):
        for j in range(begin[i],end[i]):
            times.append(i)
    return times,waitingTime




#Shortest Job First NonPreemptive
def SJF(no,burstTime,arrivalTime):
         
   n = no 
   remainingTime= 0
   begin = [None]*n
   end = [None]*n
   time = 0
   pq = []
   
   currentProcess = None
   arrivalTimeDict = dict()
   times = list()
   waitingTimes = dict()
   for i in range(0,no):
       waitingTimes[i] = 0
   #mapping process by their arrival time
   for i in range(0,n):
       if(not arrivalTimeDict.get(arrivalTime[i])):
           arrivalTimeDict[arrivalTime[i]] = list()
           arrivalTimeDict[arrivalTime[i]].append(i)
       else:
           arrivalTimeDict[arrivalTime[i]].append(i)
    
   while(n != 0):
       
        #if some process arrived at this time
       if(arrivalTimeDict.get(time)):
            #add it to the ready queue 
           for p in arrivalTimeDict.get(time):
               
               heapq.heappush(pq,(burstTime[p],p))
        #if there is no running process and there is a process or more in the ready queue
       if((currentProcess is None)and(len(pq) != 0)):
           
            #begin this process by removing it from the ready queue
           currentProcess = heapq.heappop(pq)[1]
           remainingTime = burstTime[currentProcess]
           begin[currentProcess] = time
            
        #end of Current Process
       if(remainingTime == 0 and currentProcess is not None):
           end[currentProcess] = time
           n = n-1
            #if there is a ready process begin running it
           if((len(pq) != 0)):
               currentProcess =heapq.heappop(pq)[1]
               begin[currentProcess] = time
               remainingTime = burstTime[currentProcess]
            #if not set idle
           else:
               currentProcess = None
        #advancing time of the current process
       if(currentProcess is not None):
           remainingTime = remainingTime -1
       for i in range(0,len(pq)):
           waitingTimes[pq[i][1]] += 1
       times.append(currentProcess)
        #advancing time by one quantum
           
       time = time +1
   return times,waitingTimes
   
      
# shortest Job First Preemptive   
def SJFP(no,burstTime,arrivalTime):
         
   n = no 
   intervals = dict()
   for i in range(0,n):
       intervals[i]=list()
   time = 0
   pq = []
   currentProcess = None
   arrivalTimeDict = dict()
   #initializing remainingTimes as burtTime
   remainingTimes = list()
   for t in burstTime:
       remainingTimes.append(t)
   times = list()
   waitingTimes = dict()
   for i in range(0,no):
       waitingTimes[i] = 0
       
   #mapping process by their arrival time
   for i in range(0,n):
       if(not arrivalTimeDict.get(arrivalTime[i])):
           arrivalTimeDict[arrivalTime[i]] = list()
           arrivalTimeDict[arrivalTime[i]].append(i)
       else:
           arrivalTimeDict[arrivalTime[i]].append(i)
    
   while(n != 0):
       
        #if some process arrived at this time
       if(arrivalTimeDict.get(time)):
            #add it to the ready queue 
           for p in arrivalTimeDict.get(time):
               
               heapq.heappush(pq,(burstTime[p],p))
        #if there is no running process and there is a process or more in the ready queue
       if((currentProcess is None)and(len(pq) != 0)):
           
            #begin this process by removing it from the ready queue
           currentProcess = heapq.heappop(pq)[1]
           interval = list()
           interval.append(time)
            
        #end of Current Process
       if(currentProcess is not None):
           if(remainingTimes[currentProcess] == 0):
               interval.append(time)
               intervals[currentProcess].append(interval)
               n = n-1
                #if there is a ready process begin running it
               if((len(pq) != 0)):
                   currentProcess =heapq.heappop(pq)[1]
                   interval = list()
                   interval.append(time)
                #if not set idle
               else:
                   currentProcess = None
           else:
               if((len(pq) != 0)):
                   candidate = heapq.heappop(pq)
                   # check if there is a process with a remaining time less than the current process
                   if(candidate[0] <remainingTimes[currentProcess]):
                       # if there is switch context to this process and make the current process
                       heapq.heappush(pq,(remainingTimes[currentProcess],currentProcess))
                       interval.append(time)
                       intervals[currentProcess].append(interval)
                       interval = list()
                       interval.append(time)
                       currentProcess = candidate[1]
                     #if not complete t he current process  
                   else:
                       heapq.heappush(pq,candidate)
                   
               
        #advancing time of the current process
       if(currentProcess is not None):
           remainingTimes[currentProcess] = remainingTimes[currentProcess] -1
       for i in range(0,len(pq)):
           waitingTimes[pq[i][1]] += 1
       times.append(currentProcess)     
        #advancing time by one quantum
       time = time +1
   return times,waitingTimes
 

#Priority Non Preemptive
def Priority(no,burstTime,arrivalTime,priority):
      
   
        
   n = no 
   remainingTime= 0
   begin = [None]*n
   end = [None]*n
   time = 0
   pq = []
   currentProcess = None
   arrivalTimeDict = dict()
   times = list()
   waitingTimes = dict()
   for i in range(0,no):
       waitingTimes[i] = 0
   #mapping process by their arrival time
   for i in range(0,n):
       if(not arrivalTimeDict.get(arrivalTime[i])):
           arrivalTimeDict[arrivalTime[i]] = list()
           arrivalTimeDict[arrivalTime[i]].append(i)
       else:
           arrivalTimeDict[arrivalTime[i]].append(i)
    
   while(n != 0):
       
        #if some process arrived at this time
       if(arrivalTimeDict.get(time)):
            #add it to the ready queue 
           for p in arrivalTimeDict.get(time):
               
               heapq.heappush(pq,(priority[p],p))
        #if there is no running process and there is a process or more in the ready queue
       if((currentProcess is None)and(len(pq) != 0)):
           
            #begin this process by removing it from the ready queue
           currentProcess = heapq.heappop(pq)[1]
           remainingTime = burstTime[currentProcess]
           begin[currentProcess] = time
            
        #end of Current Process
       if(remainingTime == 0 and currentProcess is not None):
           end[currentProcess] = time
           n = n-1
            #if there is a ready process begin running it
           if((len(pq) != 0)):
               currentProcess =heapq.heappop(pq)[1]
               begin[currentProcess] = time
               remainingTime = burstTime[currentProcess]
            #if not set idle
           else:
               currentProcess = None
        #advancing time of the current process
       if(currentProcess is not None):
           remainingTime = remainingTime -1
       for i in range(0,len(pq)):
           waitingTimes[pq[i][1]] += 1
       times.append(currentProcess)    
            
        #advancing time by one quantum
       time = time +1
   return times,waitingTimes  

#print(Priority(n,burstTime,arrival,priority)  )        
   

#Priority Preemptive         
def PriorityP(no,burstTime,arrivalTime,priority):      
   n = no 
   intervals = dict()
   for i in range(0,n):
       intervals[i]=list()
   time = 0
   pq = []
   currentProcess = None
   arrivalTimeDict = dict()
   #initializing remainingTimes as burtTime
   remainingTimes = list()
   for t in burstTime:
       remainingTimes.append(t)
   times = list()
   waitingTimes = dict()
   for i in range(0,no):
       waitingTimes[i] = 0
       
   #mapping processes by their arrival time
   for i in range(0,n):
       if(not arrivalTimeDict.get(arrivalTime[i])):
           arrivalTimeDict[arrivalTime[i]] = list()
           arrivalTimeDict[arrivalTime[i]].append(i)
       else:
           arrivalTimeDict[arrivalTime[i]].append(i)
    
   while(n != 0):
       
        #if some process arrived at this time
       if(arrivalTimeDict.get(time)):
            #add it to the ready queue 
           for p in arrivalTimeDict.get(time):
               
               heapq.heappush(pq,(priority[p],p))
        #if there is no running process and there is a process or more in the ready queue
       if((currentProcess is None)and(len(pq) != 0)):
           
            #begin this process by removing it from the ready queue
           currentProcess = heapq.heappop(pq)[1]
           interval = list()
           interval.append(time)
            
        #end of Current Process
       if(currentProcess is not None):
           if(remainingTimes[currentProcess] == 0):
               interval.append(time)
               intervals[currentProcess].append(interval)
               n = n-1
                #if there is a ready process begin running it
               if((len(pq) != 0)):
                   currentProcess =heapq.heappop(pq)[1]
                   interval = list()
                   interval.append(time)
                #if not set idle
               else:
                   currentProcess = None
           else:
               if((len(pq) != 0)):
                   candidate = heapq.heappop(pq)
                   # check if there is a process with a remaining time less than the current process
                   if(candidate[0] <priority[currentProcess]):
                       # if there is switch context to this process and make the current process
                       heapq.heappush(pq,(priority[currentProcess],currentProcess))
                       interval.append(time)
                       intervals[currentProcess].append(interval)
                       interval = list()
                       interval.append(time)
                       currentProcess = candidate[1]
                     #if not complete t he current process  
                   else:
                       heapq.heappush(pq,candidate)
                   
               
        #advancing time of the current process
       if(currentProcess is not None):
           remainingTimes[currentProcess] = remainingTimes[currentProcess] -1
       for i in range(0,len(pq)):
           waitingTimes[pq[i][1]] += 1
       times.append(currentProcess)    
        #advancing time by one quantum
       time = time +1
   
   return times,waitingTimes            
        

def RR(no,burstTime,arrivalTime,quantum):
    currentProcess = None
    remainingTime = 0
    quantumLeft = 0
    times = list()
    readyQueue = list()
    arrivalTimeDict = dict()
    n = no
    time = 0
    waitingTimes = dict()
    for i in range(0,no):
        waitingTimes[i] = 0
    
    for i in range(0,n):
       if(not arrivalTimeDict.get(arrivalTime[i])):
           arrivalTimeDict[arrivalTime[i]] = list()
           arrivalTimeDict[arrivalTime[i]].append(i)
       else:
           arrivalTimeDict[arrivalTime[i]].append(i)
           
   
    while(n != 0):
        if(arrivalTimeDict.get(time)):
            #add it to the ready queue 
           for p in arrivalTimeDict.get(time):
               
               readyQueue.insert(0,[p,burstTime[p]])
               
        done = False
        
        #if there is a process and it's done decreament the no of processes
        if(remainingTime ==0 and currentProcess is not None):
            done = True
            n -= 1
        #if it's not done yet but it's the end of the current session 
        # add it again to the ready queue with the remaining time
        if(not done and quantumLeft ==0 and currentProcess is not None):
            readyQueue.insert(0,[currentProcess,remainingTime])
        # switch context: pop a process from the ready queue and initialize the session
            # if the current process is done
            # or the session is done
            # or there is no porcess @ all
        if(done or quantumLeft==0 or (currentProcess is None)):
            # assertion: if there is at least one process in the ready queue
            if(len(readyQueue)!=0):
                Process = readyQueue.pop()
               
                currentProcess = Process[0]
                remainingTime = Process[1]
                quantumLeft = quantum
        #record that @ this time the current process is:
        times.append(currentProcess)
        for i in range(0,len(readyQueue)):
           waitingTimes[readyQueue[i][0]] += 1
        if(currentProcess is not None):
            remainingTime -=1
            quantumLeft -=1

        time += 1
        
    return times,waitingTimes
        
        
        
    

#no = 3
#burstTime = [24,3,3]
#arrival =[0,0,0]
#quantum = 4
#print(RR(no,burstTime,arrival,quantum)) 


           
#print(PriorityP(n,burstTime,arrival,priority)  )              
           
   
   
   
    
#SJFP(n,burstTime,arrival)
def stringListToInt(T):
    t = list()
    T = T.split()
    for i in range(0, len(T)):
        t.append(int(T[i]))
    return t   
    
def plotGannt(l):
    y = list()
    x = list()
    for i in range(0,len(l)):
        if(l[i] == None):
            y.append(0)
        else:
            y.append(l[i]+1)
        x.append(i)
    plt.figure("CPU") 
    plt.xlabel('Time')
    plt.ylabel('Process')   
    plt.plot(x,y,'ro')
    plt.xticks(x)
    plt.yticks(np.arange(min(y), max(y)+1, 1.0))
    plt.show()
 

    
###################
#Test Case 1: FCFS#
###################
#no = 3
#arrivalTime = [0,0,0]
#burstTime = [24,3,3]

###################
#Test Case 2: SJF#
###################
#no = 4
#arrivalTime = [0,0,0,0]
#burstTime = [6,8,7,3]

###################
#Test Case 3: SJFP#
###################
#no = 4
#arrivalTime = [0,1,2,3]
#burstTime = [8,4,9,5]

###################
#Test Case 4: Priority#
###################
#no = 3
#arrivalTime = [0,1,2]
#burstTime = [10,1,2]
#priority

###################
#Test Case 5: Priority#
###################
#no = 5
#arrivalTime = [0,1,2,3,4]
#burstTime = [10,1,2,1,5]
#priority = [3,1,4,5,2]

###################
#Test Case 6: PriorityP#
###################
#no = 5
#arrivalTime = [0,1,2,3,4]
#burstTime = [10,1,2,1,5]
#priority = [3,1,4,5,2]

###################
#Test Case 7: round robin#
###################
#no = 3
#arrivalTime = [0,0,0]
#burstTime = [24,3,3]
#quantum time = 4

noS = input('enter No of Process: ')
arrivalTimeS = input('enter Arrival Time for each process (sperated by Spaces): \n')
burstTimeS = input('enter Burst Time for each process (sperated by Spaces): \n')
no = int(noS)
arrivalTime = stringListToInt(arrivalTimeS)
burstTime = stringListToInt(burstTimeS)
algorithm = input('specify the scheduling algorithm: \n-f for FCFS.\n-s for SJF.\n-sp for SJF Preemptive.\n-p for Priority.\n-pp for Priority Preemptive.\n-r for RoundRoubin.\n')
times = list()
waitingTimes = dict()
if(algorithm == '-f'):
    times,waitingTime = FCFS(no,burstTime,arrivalTime)
elif(algorithm=='-s'):
    times,waitingTimes = SJF(no,burstTime,arrivalTime)
    waitingTime = avgWaitingTime(waitingTimes)
elif(algorithm=='-sp'):
    times,waitingTimes = SJFP(no,burstTime,arrivalTime)
    waitingTime = avgWaitingTime(waitingTimes)
elif(algorithm=='-p'):
    priorityS = input('enter Priority for each process (sperated by Spaces): \n')
    priority = stringListToInt(priorityS)
    times,waitingTimes = Priority(no,burstTime,arrivalTime,priority)
    waitingTime = avgWaitingTime(waitingTimes)
elif(algorithm=='-pp'):
    priority = input('enter Priority for each process (sperated by Spaces): \n')
    priority = stringListToInt(priorityS)
    times,waitingTimes = PriorityP(no,burstTime,arrivalTime,priority)
    waitingTime = avgWaitingTime(waitingTimes)
elif(algorithm=='-r'):
    quantumS = input('specify quantum time: \n')
    quantum = int(quantumS)
    times,waitingTimes = RR(no,burstTime,arrivalTime,quantum)
    waitingTime = avgWaitingTime(waitingTimes)
        
plotGannt(times)
print('Average Waiting Time: ', waitingTime)
        
 
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
           
  
