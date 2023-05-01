import boto
import boto3
import json
import time
import threading
import re
import parser
import os
import argparse
import pdb


def receivemessage(workername):

    print("Starting thread: " + workername)

    sqs = boto3.resource('sqs')
    SQSQ = sqs.get_queue_by_name(QueueName=QNAME)

    no_of_messages = SQSQ.attributes['ApproximateNumberOfMessages']

    while int(no_of_messages) > 0 :
        
        try:
            messages=SQSQ.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=20)
        except Exception as e:
            print(e)
            print("Failed to receive message from primary queue")
            exit(1)

        print ("Number of messages in Queue: " + no_of_messages)

        for message in messages:
            msgbody = message.body

            if re.search(r''+SEARCH_STRING, msgbody):
                with open(workername+'.json', 'a') as outfile:
                    outfile.writelines(message.body)
                    outfile.write("\n")
                    # Mark the message as deleted if delete flag is set
                    if DELETE:
                        message.delete()   
                    outfile.close()            
            else:
                pass
                # print("Message does not contain "+SEARCH_STRING+ " ignoring..")

                # uncomment the following block if you want to keep records of the messages that are not matching
                # with open(workername+'-normal.json', 'a') as outfile:
                #     outfile.writelines(message.body)
                #     outfile.write("\n")
                #     # Mark the message as deleted 
                #     outfile.close() 
                
        
        no_of_messages = SQSQ.attributes['ApproximateNumberOfMessages']


if __name__ == '__main__':

    # argparse - get number of threads and search string
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads", help="Number of threads to spawn", type=int)
    parser.add_argument("-s", "--search", help="Search string to look for in the message body", type=str)
    parser.add_argument("-q", "--queue", help="Name of the queue to read from", type=str)
    parser.add_argument("-d", "--delete", help="Delete the message from the queue after reading", type=bool)
    args = parser.parse_args()

    parser.error = lambda err: print("Usage: python InFlightSQS.py -t <number of threads> -s <search string> -q <queue name> -d <delete message from queue>")

    

    # Check if the inputs are provided or print usage
    if not args.threads or not args.search or not args.queue or not args.delete:
        print("Usage: python InFlightSQS.py -t <number of threads> -s <search string> -q <queue name> -d <delete message from queue>")
        exit(1)

    # Check the datatype of the inputs
    if not isinstance(args.threads, int) or not isinstance(args.search, str) or not isinstance(args.queue, str) or not isinstance(args.delete, bool):
        print("Usage: python InFlightSQS.py -t <number of threads> -s <search string> -q <queue name> -d <delete message from queue>")
        exit(1)

    # Print the inputs
    print("Number of threads: " + str(args.threads))
    print("Search string: " + args.search)
    print("Queue name: " + args.queue)
    print("Delete flag: " + str(args.delete))
    
    # Check the inputs for valid values
    if args.threads < 1 or args.threads > 10:
        print("Number of threads should be between 1 and 10")
        exit(1)
    elif args.search == "":
        print("Search string cannot be empty")
        exit(1)
    elif args.queue == "":
        print("Queue name cannot be empty")
        exit(1)
    elif args.delete == "True" or args.delete == "False":
        print("Delete flag cannot be empty and should be either True or False")
        exit(1)

    SEARCH_STRING = args.search
    NUM_THREADS = args.threads
    QNAME = args.queue
    DELETE = args.delete

    
    # Create threads as per the number of threads specified
    for i in range(NUM_THREADS):
        t = threading.Thread(target=receivemessage, args=("worker-"+str(i),))
        t.start()
        time.sleep(1)
    
    # Wait for all threads to finish
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()