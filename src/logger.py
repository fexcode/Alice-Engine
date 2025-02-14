from rich import console

csl = console.Console()


class Logger:
    def __init__(self, debug=False):
        self.debug = debug

    def warn(self, message):
        if self.debug:
            csl.print(message, style="bold yellow")

    def error(self, message):
        if self.debug:
            csl.print(message, style="bold red")
    
    def info(self, message):
        if self.debug:
            csl.print(message, style="bold blue")

    def success(self, message):
        if self.debug:
            csl.print(message, style="bold green")
    
    def log(self, message):
        if self.debug:
            csl.log(message)


logger = Logger(debug=True)
