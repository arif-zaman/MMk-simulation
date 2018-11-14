
	# CSE411 - Simulation and Modeling

"""
The task is to simulate a M/M/k system with a single queue.
Complete the skeleton code and produce results for three experiments.
The study is mainly to show various results of a queue against its ro parameter.
ro is defined as the ratio of arrival rate vs service rate.
For the sake of comparison, while plotting results from simulation, also produce the analytical results.
"""

import heapq
import random
import matplotlib.pyplot as plt

class Customer:
    def __init__(self,arrival_time,service_start_time,service_time):
        self.arrival_time=arrival_time
        self.service_start_time=service_start_time
        self.service_time=service_time
        self.service_end_time=self.service_start_time+self.service_time
        self.wait=self.service_start_time-self.arrival_time


# Generate Random Sample from negative exponential
def neg_exp(lambd):
    return random.expovariate(lambd)


def printResults(Customers,simclock,lambd,mu):
    Waits=[a.wait for a in Customers]
    avgQdelay=sum(Waits)/len(Waits)

    served = len(Customers)
    Total_Times = [a.wait+a.service_time for a in Customers]
    Mean_Time = sum(Total_Times)/len(Total_Times)
    avgQlength = (Mean_Time/float(simclock)) * served
    Service_Times=[a.service_time for a in Customers]

    if sum(Service_Times) >= simclock:
        util = 1
    else:
        util=sum(Service_Times)/simclock

    # Output Result
    print 'MMk Results: lambda = %lf, mu = %lf, k = %d' % (lambd,mu,1)
    print 'MMk Total customer served: %d' % served
    print 'MMk Average queue length: %lf' % avgQlength
    print 'MMk Average customer delay in queue: %lf' % avgQdelay
    print 'MMk Time-average server utility: %lf' % util


def getResults(Customers,simclock):
    Waits=[a.wait for a in Customers]
    avgQdelay=sum(Waits)/len(Waits)

    served = len(Customers)
    Total_Times = [a.wait+a.service_time for a in Customers]
    Mean_Time = sum(Total_Times)/len(Total_Times)
    avgQlength = (Mean_Time/float(simclock)) * served

    Service_Times=[a.service_time for a in Customers]
    if sum(Service_Times) >= simclock:
        util = 1
    else:
        util=sum(Service_Times)/simclock

    # Return Result for Plotting
    return avgQlength,avgQdelay,util

def MMK(lambd,mu,k,option):
    # Simulation Time
    simulation_time = 300
    simclock=0
    Customers=[]

    last_k_Customer = []
    while simclock<simulation_time:
        if len(Customers)<=k:
            arrival_time=neg_exp(lambd)
            service_start_time=arrival_time
        else:
        	arrival_time+=neg_exp(lambd)
        	k_customer = last_k_Customer[len(last_k_Customer)-k:]
        	service_start_time=max(arrival_time,min(k_customer))

        service_time = neg_exp(mu)
        end_time = service_start_time + service_time
        last_k_Customer.append(end_time)

        # Add new Customer
        if arrival_time <=simulation_time and end_time <= simulation_time:
            Customers.append(Customer(arrival_time,service_start_time,service_time))

        # Increment clock till next end of service
        if arrival_time <= simulation_time:
            simclock=arrival_time
        else:
            simclock = simulation_time

    if option == 2:
        # Calculate and Return Results
        return getResults(Customers,simclock)
    else:
        # Calculate and Print Results
        printResults(Customers,simclock,lambd,mu)


def experiment1():
	seed = 101
	MMK(5.0/60, 8.0/60,1,1)

def experiment2():
    seed = 110
    mu = 1000.0 / 60
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    for ro in ratios:
        length, delay, utl = MMK(mu*ro, mu, 1, 2)
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(ratios, avglength)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(ratios, avgdelay)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(ratios, util)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Util')

    plt.suptitle('Experiment 2', fontsize=16)
    plt.show()

def experiment3():
	# Similar to experiment2 but for different values of k; 1, 2, 3, 4
	# Generate the same plots
    seed = 111
    mu = 1000.0 / 60
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    k = 1
    for ro in ratios:
        length, delay, utl = MMK(mu*ro, mu, k, 2)
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)
        k=k+1

    plt.figure(1)
    plt.subplot(311)
    plt.plot(ratios, avglength)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q length')


    plt.subplot(312)
    plt.plot(ratios, avgdelay)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(ratios, util)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Util')

    plt.suptitle('Experiment 3', fontsize=16)
    plt.show()

def main():
    print "Experiment 1 Results:\n"
    experiment1()
    print "\nExperiment 2:\n \t now plotting ......."
    experiment2()
    print "\nExperiment 3:\n \t now plotting ...... "
    experiment3()


if __name__ == "__main__":
    main()