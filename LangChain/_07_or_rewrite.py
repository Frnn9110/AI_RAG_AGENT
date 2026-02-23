class MySqueue(object):
    def __init__(self, *args):
        self.squeue = []
        for arg in args:
            self.squeue.append(arg)

    def __or__(self, other):
        self.squeue.append(other)
        return self

    def run(self):
        for arg in self.squeue:
            print(arg)


class Test(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __or__(self, other):
        return MySqueue(self.name, other)



if __name__ == '__main__':
    a = Test('a')
    b = Test('b')
    c = Test('c')

    d = a | b | c

    d.run()
