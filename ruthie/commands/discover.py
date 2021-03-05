from .base import Base
from ruthie.toolset import discoverer


class Discover(Base):

    def run(self):
        if self.options['classes']:
            if self.options['--group']:
                self.print_classes_grouped()
            else:
                self.print_classes_listed()
        else:
            raise AttributeError('Unsupported command')

    def print_classes_grouped(self):
        last = None
        for discovery in discoverer.classes_in(self.options['<path>']):
            if last != discovery[0]:
                print(f'  {discovery[0]}')
                last = discovery[0]
            print(f'    {discovery[1]}')

    def print_classes_listed(self):
        for discovery in discoverer.classes_in(self.options['<path>']):
            print(f'{discovery[0]}.{discovery[1]}')
