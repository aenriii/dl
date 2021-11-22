

class Logger:
    prefix: str
    doClearLine: bool 

    def __init__(this, prefix: str = '', doClearLine: bool = True):
        this.prefix = prefix
        this.doClearLine = doClearLine
    def log(this, *args):
        message = ''
        if this.doClearLine:
            print('\b' * 100 + '\r')
        if this.prefix:
            message += '[' + this.prefix + ']'
        for arg in args:
            message += ' ' + arg
        print(message)

        