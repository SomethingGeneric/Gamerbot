import os


def get_stamp():
    os.system("date >> stamp")
    with open("stamp") as f:
        s = f.read()
    os.remove("stamp")
    return s


class BotLogger:
    def __init__(self, filename):

        if os.path.exists(filename):
            n = 0
            while os.path.exists(filename + "." + str(n)):
                n += 1
            filename = filename + "." + str(n)

        self.fn = filename

    def log(self, caller, text):
        info = get_stamp().strip() + " --> " + caller + ": " + text
        with open(self.fn, "a+") as f:
            f.write("\n" + info + "\n")
        print(info)

    def get_log(self):
        with open(self.fn) as f:
            return f.read()
