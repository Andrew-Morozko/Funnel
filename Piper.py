import threading
from abc import ABCMeta, abstractmethod


class Piper(metaclass=ABCMeta):
    """ Abstract class for every sevice piper """

    def __init__(self, source, dest):
        """ Queues direction relative to handler """

        # Received messages
        self.in_q = source.out_q

        # Converted messages
        self.out_q = dest.in_q

        # Thread for converter
        self.converter_thread = threading.Thread(target=self.converter, args=(self.in_q, self.out_q))

        self.converter_thread.start()

    @abstractmethod
    def converter(self, in_q, out_q):
        pass
