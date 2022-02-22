from datetime import datetime

def get_now():
    now = datetime.now()
    timestamp = "%04d/%02d/%02d_%02d:%02d:%02d" %(now.year, now.month, now.day, now.hour, now.minute, now.second)
    return timestamp


def log(filename, content):
    with open(filename, "a") as o:
        o.write("%s\t%s\n" %(get_now(), content))
    return
