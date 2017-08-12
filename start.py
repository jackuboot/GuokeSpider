from multiprocessing import Process, Manager, Pool
from Producer.producer import Creator
from Consumer.consumer import Consumr  
import os, time


if __name__ == "__main__":
	#get cretor instance
	creator = Creator()
	print "1"
	#get consumer instance
	consumr = Consumr()

	#create Shared queue
	manager = Manager()
	queue = manager.Queue()#use Method not a attribute,if use manager.Quenue,there will get a wrong
	pools = Pool()
	print "2"

	#create producter
	input_1 = pools.apply_async(creator.input_data(queue))#, args=(queue))
	input_2 = pools.apply_async(consumr.get_data(queue))#,   args=(queue))	
	pools.close()
	pools.join()
	print "3"
	#create Consumer
    #consumer_process = Process(target=get_data_, args=(q,))
