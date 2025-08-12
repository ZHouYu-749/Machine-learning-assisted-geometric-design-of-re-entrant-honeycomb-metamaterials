from odbAccess import openOdb
from abaqusConstants import *
import os
import csv

dir_path = r'C:\Users\PC\Desktop\work2\odb\odb2'  
output_dir = r'C:\Users\PC\Desktop\work2\odb\csv' 

odb_files = [f for f in os.listdir(dir_path) if f.endswith('.odb')]


for file_name in odb_files:
    file_path = os.path.join(dir_path, file_name)
    my_odb = openOdb(file_path)
    step = my_odb.steps['Step-1']
    history_region = step.historyRegions['Node YABAN-1.442']
    displacement_history_U2 = history_region.historyOutputs['U2']
    reaction_force_history_RF2 = history_region.historyOutputs['RF2']

  
    output_file_name = os.path.splitext(file_name)[0] + '.csv' 
    merged_file_path = os.path.join(output_dir, output_file_name)

 
    time_U2, displacement_U2 = [], []
    time_RF2, reaction_force_RF2 = [], []

 
    for point in displacement_history_U2.data:
        time_U2.append(point[0])
        displacement_U2.append(point[1])

    for point in reaction_force_history_RF2.data:
        time_RF2.append(point[0])
        reaction_force_RF2.append(point[1])


    merged_data = []
    for t, u, rf in zip(time_U2, displacement_U2, reaction_force_RF2):
        merged_data.append([t, -u, -rf])


    with open(merged_file_path, 'wb') as f_merged:
        writer = csv.writer(f_merged)
        writer.writerow(['Time', 'U2', 'RF2'])
        for row in merged_data:
            writer.writerow(row)
    my_odb.close()




'''
from odbAccess import openOdb
from abaqusConstants import *
import os

file_name = '60mm_1_001.odb'
dir_path = r'C:/Users/PC/Desktop/odb'
file_path = os.path.join(dir_path, file_name)
my_odb = openOdb(file_path)
step = my_odb.steps['Step-1']
print(step.historyRegions)

'''