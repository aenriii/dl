from sys import stdout


class Logger:
    prefix: str
    doClearLine: bool
    doPrint: bool

    def __init__(this, prefix: str = '', doClearLine: bool = False):
        this.prefix = prefix
        this.doClearLine = doClearLine
        this.doPrint = True

    def log(this, *args):
        message = ''
        if this.doClearLine:
            this.print('\b' * 100 + '\r')
        else:
            message += '\n'
        if this.prefix:
            message += '[' + this.prefix + ']'
        for arg in args:
            message += ' ' + str(arg)
        if this.doPrint:
            this.print(message)

    def print(self, message: str):
        stdout.write(message)
        stdout.flush()
