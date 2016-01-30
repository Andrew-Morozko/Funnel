import threading
import queue
from abc import ABCMeta, abstractmethod


class Handler(metaclass=ABCMeta):
    """ Abstract class for every sevice handler """

    def __init__(self):
        """ Queues direction relative to handler """

        # Messages to send
        self.in_q = queue.Queue()

        # Received messages
        self.out_q = queue.Queue()

        # Threads for sender and receiver
        self.receiver_thread = threading.Thread(target=self.receiver, args=(self.out_q, ))
        self.sender_thread   = threading.Thread(target=self.sender,   args=(self.in_q, ))

        self.receiver_thread.start()
        self.sender_thread.start()

    @abstractmethod
    def receiver(self, q):
        pass

    @abstractmethod
    def sender(self, q):
        pass
