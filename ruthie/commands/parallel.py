import importlib
import threading
from unittest import TestSuite, TestLoader

from xmlrunner import xmlrunner

from ruthie.toolset import discoverer
from .base import Base


class Parallel(Base):
    threads = None
    queue = None

    def run(self):
        assert self.options['--threads'].isdigit(), "Threads must be a number"

        self.threads = int(self.options['--threads'])
        assert self.threads > 1, "Threads number must be greater than 1"

        self.queue = discoverer.classes_in(self.options['<path>'])

        for i in range(self.threads):
            t = threading.Thread(target=self.run_tests)
            t.start()

    def run_tests(self):
        while len(self.queue) > 0:
            print("Taking from queue...")
            test_params = self.queue.pop()

            print(f"Importing {test_params[0]}")
            module_object = importlib.import_module(test_params[0])
            test_class = getattr(module_object, test_params[1])
            loader = TestLoader()
            suite = TestSuite(
                (
                    loader.loadTestsFromTestCase(test_class)
                )
            )

            print(f"Running {test_params[0]}.{test_params[1]}")
            runner = xmlrunner.XMLTestRunner(output="junit", verbosity=2)
            runner.run(suite)
