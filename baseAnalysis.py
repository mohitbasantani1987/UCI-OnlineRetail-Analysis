from abc import ABC, abstractmethod

'''This is an abstract base class which will be used to define the interface for main Class.'''

class BaseAnalysis(ABC):

    @abstractmethod
    def run_analysis(self):
        """
        This method should be implemented by main class to perform the analysis.
        """
        pass