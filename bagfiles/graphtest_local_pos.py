import csv
import matplotlib.pyplot as plt

time_stamp = []
posx_stamp = []
posy_stamp = []
"""
In the data.txt converted from .bag file,the time 
is in position 0 in the row.
The X-value is in position 4
The Y-value is in position 5
"""
time_stamp_temp =[]
x_pos_temp = []
y_pos_temp = []
with open('local_pos_data.txt','r') as file:
    reader = csv.reader(file)
    for row in reader:
        time_stamp_temp.append(row[0])
        x_pos_temp.append(row[4])
        y_pos_temp.append(row[5])
for i in range(1, len(time_stamp_temp)):
    time_stamp.append(float(time_stamp_temp[i]))
    posx_stamp.append(float(x_pos_temp[i]))
    posy_stamp.append(float(y_pos_temp[i]))

print(time_stamp)
print(posy_stamp)
print(posx_stamp)

time_stamp_global = []
posx_stamp_global= []
posy_stamp_global = []
"""
In the global_local_data.txt converted from .bag file,the time 
is in position 0 in the row.
The X-value is in position 5
The Y-value is in position 6

"""
time_stamp_global_temp =[]
x_pos_temp_global = []
y_pos_temp_global= []


with open('global_local_data.txt','r') as file:
    reader = csv.reader(file)
    for row in reader:
        time_stamp_global_temp.append(row[0])
        x_pos_temp_global.append(row[5])
        y_pos_temp_global.append(row[6])
for i in range(1, len(time_stamp_global_temp)):
    time_stamp_global.append(float(time_stamp_global_temp[i]))
    posx_stamp_global.append(float(x_pos_temp_global[i]))
    posy_stamp_global.append(float(y_pos_temp_global[i]))

print(time_stamp_global)
print(posy_stamp_global)
print(posx_stamp_global)
plt.subplot(221)
plt.plot(time_stamp,posx_stamp)
plt.ylabel('Local Pos X')
plt.xlabel('Time Stamp')
plt.subplot(222)
plt.plot(time_stamp,posy_stamp)
plt.ylabel('Local Pos Y')
plt.xlabel('Time Stamp')
plt.subplot(223)
plt.plot(time_stamp_global,posx_stamp_global)
plt.ylabel('Global Pos X')
plt.xlabel('Time Stamp')
plt.subplot(224)
plt.plot(time_stamp_global,posy_stamp_global)
plt.ylabel('Global Pos Y')
plt.xlabel('Time Stamp')
plt.show()