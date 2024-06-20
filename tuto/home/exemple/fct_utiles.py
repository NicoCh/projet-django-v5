from time import strptime
from datetime import time, timedelta, date, datetime

def interfere(colle1, colle2):
    """
    :param colle1: Première colle
    :param colle2: Deuxième colle
    :return: Vrai si les deux colles interférent et faux sinon
    """
    if colle1[2] == colle2[2]:
        t = strptime(colle1[3], "%H:%M")
        dt = strptime(colle1[4], "%H:%M")
        deb1 = datetime.combine(date(1, 1, 1), time(
            hour=t.tm_hour, minute=t.tm_min))
        fin1 = deb1 + timedelta(hours=dt.tm_hour, minutes=dt.tm_min)
        t = strptime(colle2[3], "%H:%M")
        dt = strptime(colle2[4], "%H:%M")
        deb2 = datetime.combine(date(1, 1, 1), time(
            hour=t.tm_hour, minute=t.tm_min))
        fin2 = deb2 + timedelta(hours=dt.tm_hour, minutes=dt.tm_min)
        if deb1 <= deb2 < fin1 or deb1 < fin2 <= fin1 or deb2 <= deb1 < fin2 or deb2 < fin1 <= fin2:
            return True
    return False
