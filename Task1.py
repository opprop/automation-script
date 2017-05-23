import json
import os
import inspect
import csv

abs_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
os.chdir(current_dir)

with open('corpus.json') as json_file:
  json_object = json.load(json_file)
    
projects = json_object['projects']

metrics_store = []

os.chdir(abs_path) 
with open('data.csv','w+') as csvfile_write:
 
    for project in projects:

        csvfile_write.write(','  + project)

    for project in projects:
 
 	#os.chdir(abs_path + '/corpus/' + project)

 	#os.system(projects[project]['clean'])
 	#os.system(abs_path + '/pascaliUWat/ontology/run-dljc.sh ' + projects[project]['build'])


        os.chdir(abs_path + '/corpus/' + project)
  

        with open('solver-statistic.txt') as data_file:

            for line in data_file.readlines():
	
               l = line.strip().split(',')
               metrics = l[0]
	       number = l[1] 
               if(metrics not in metrics_store):
                  metrics_store.append(metrics)
               
   
    h = len(metrics_store)
    w = len(projects)  
    table = [[0 for x in range(w)] for y in range(h)]
    table[metrics_store][0]
        
       
        
       
   

























          
	 
