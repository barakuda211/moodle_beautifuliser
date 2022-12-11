import shutil
import os
import csv
import codecs
import zipfile

files = os.listdir(os.curdir)
students = {}
for file in files:
    if file.endswith('.csv'):
        with codecs.open(file, 'r',encoding='utf8' ) as File:
            reader = csv.reader(File)
            first = False
            for row in reader:
                if not first:
                    first = True
                    continue
                try:
                    name = row[1] + ' ' + row[0]
                    group = row[2].split()[0]
                    students[name] = group
                except:
                    print("\nWarning! Can`t parse .csv row:")
                    line = ""
                    for word in row:
                        line += word + " "
                    print(line)
        break
print("Students initialized")

temp_dir = os.curdir+"/temp/"
os.mkdir(temp_dir)
for file in files:
    if file.endswith('.zip'):
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        break
print("Data unzipped")

result_dir = os.curdir+"/result/"
if os.path.exists(result_dir):
    shutil.rmtree((result_dir))
os.mkdir(result_dir)
for group in students.values():
    if not os.path.exists(result_dir + group):
        os.mkdir(result_dir + group)
for stud in students.keys():
    if not os.path.exists(result_dir + students[stud] + "/" + stud):
        os.mkdir(result_dir + students[stud] + "/" + stud)

tasks_dirs = os.listdir(temp_dir)
for task_dir in tasks_dirs:
    number = task_dir.split(" - ")[0].lstrip("Q")
    task_text = temp_dir+task_dir+"/Question text"
    students_dirs = os.listdir(temp_dir+task_dir)
    for student_dir in students_dirs:
        name = ""
        try:
            if student_dir == 'Question text':
                continue
            name = student_dir.split(" - ")[1]
        except:
            print("\nError in parsing tasks")
            print("Task dir: "+task_dir)
            print("Student dir: "+student_dir)
            #exit(-1)                                                               
            continue
        files = os.listdir(temp_dir+task_dir+"/"+student_dir)
        for file in files:
            shutil.copy(temp_dir+task_dir+"/"+student_dir+"/"+file, result_dir + students[name] + "/" + name +"/"+file)
        shutil.copy(task_text, result_dir + students[name] + "/" + name + "/Question text "+number)

shutil.make_archive('out', 'zip', result_dir)

shutil.rmtree(temp_dir)


