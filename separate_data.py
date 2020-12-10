from csv import reader
from contextlib import ExitStack
import os
class_names = list(range(201))
with open("AIS_2019_01_01_inverted.csv","r") as read_obj:
    with ExitStack() as stack:
        files = [stack.enter_context(open(str(class_name)+".csv","a")) for class_name in class_names]
        csv_reader = reader(read_obj)
        for row in csv_reader:
            label = row[10]
            if label == "":
                label = 200
            else:
                label = int(label)
            try:
                label = class_names.index(label)
            except:
                print(row)
                exit(1)
            files[label].write(",".join(row))
            files[label].write("\n")
        for stack in files:
            stack.close()
# Cleanup
with ExitStack() as stack:
    files = [stack.enter_context(open(str(class_name)+".csv","a")) for class_name in class_names]
    for filea in files:
        size = os.stat(filea.fileno()).st_size
        if(size == 0):
            filea.close()
            os.remove(filea.name)
