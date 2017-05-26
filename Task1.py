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
index_m = 1
index_p = 1
metrics_filter = []
indicator = 0

os.chdir(abs_path) 

with open('data.csv','w+') as csvfile:

      
    for project in projects:
 
        os.chdir(abs_path + '/corpus/' + project)

 	os.system(projects[project]['clean'])
 	os.system(abs_path + '/pascaliUWat/ontology/run-dljc.sh ' + projects[project]['build'])


        os.chdir(abs_path + '/corpus/' + project)
  

        with open('solver-statistic.txt') as data_file:

            for line in data_file.readlines():
	
                l = line.strip().split(',')
                metrics = l[0]
	       
                if(metrics not in metrics_filter):
                    metrics_filter.append(metrics)


    height = len(metrics_filter)
    width = len(projects)  
    table = [[' ' for x in range(width+1)] for y in range(height+1)]

    for project in projects:
    
        os.chdir(abs_path + '/corpus/' + project)

        with open('solver-statistic.txt') as data_file2:

              
            for line in data_file2.readlines():

                n = line.strip().split(',')
	        metrics2 = n[0]
                number2 = n[1]
                metrics_index = 1

	        for metrics in metrics_filter: 

	            if(metrics == metrics2):
                        table[metrics_index][index_p] = number2
		        break
		    metrics_index += 1

            table[0][index_p] = project
	    index_p += 1
	    
	   
    for metrics in metrics_filter:
        
        table[index_m][0] = metrics
	index_m += 1

    writer = csv.writer(csvfile)
    [writer.writerow(r) for r in table]


    
















   





















	
        
       
        
       
   

























          
	 
