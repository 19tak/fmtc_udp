from datetime import datetime, timedelta
import time

while True:
    stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    stime2 = datetime.strptime(stime,'%Y-%m-%d %H:%M:%S.%f')

    # print(stime, stime2)

    ntime = datetime.utcnow()
    dtime =  abs(stime2 - ntime)

    # print(datetime.strftime(dtime,'%S.%f'))

    test = str(dtime)
    test2 = datetime.strptime(test,'%H:%M:%S.%f')

    print(test2)
    # print(float(test))

print("end")