import json
import os
import commands
import csv
import datetime
import pygal
from pygal.style import Style

currentDT = datetime.datetime.now() 
time = currentDT.strftime("%Y/%m/%d %H:%M:%S")
file_dir = os.getcwd()
 
with open('corpus.json') as json_file:
    json_object = json.load(json_file)
    projects = json_object['projects']

def Run_inference():

    infer_result = {}
    with open('corpus.json') as json_file:
        json_object = json.load(json_file)
        projects = json_object['projects'] 

    for project in projects:
 
        os.chdir(file_dir + '/corpus/' + project)    
        os.system(projects[project]['clean'])                                   #Clean projects
        os.system(file_dir + '/ontology/run-dljc.sh ' 
        + projects[project]['build'])                                           #Build projects
       
        with open('solver-statistic.json') as data_file:
            json_keys = json.load(data_file)                                                    
        infer_result.update({project:json_keys})                                #Store inferrence all results into "infer_result" 

    return(infer_result)

def Make_datafile(new_result):
    data_dict= {}                                          
    os.chdir(file_dir)
    try:
        with open('inferrence-data.json', 'r') as json_file:                    #Load past statistical data from inferrence-data.json file
	    json_data = json.load(json_file)
	    data_dict.update(json_data)                                         #Load past statistical data into "data_dict" dictionary
	    data_dict[time] = new_result                                        #Combine new statistical data to old data by appending new statistical data into "data_dict" dictionary
   	    with open('inferrence-data.json','w') as json_file:
                json.dump(data_dict, json_file, indent=4)
    except:                                                                     #Generates a new "inferrence-data.json" file if it doesn't exist in directory(meaning that there is no past statistical information)
        with open('inferrence-data.json','w+') as json_file:
            data_dict = {time:new_result}
            json.dump(data_dict, json_file, indent=4)

    return data_dict

def Generate_graph(data): 
    projects_store = []
    metrics_store = []

    custom_style = Style(title_font_size=30)                                        
    for time in data:
        for project in data[time]:
            if(project not in projects_store):
                projects_store.append(project)

    for project in projects_store:
        time_store = []
        for time in data:
            if(json.dumps(project in data[time].keys())):
	        time_store.append(time)
        time_store.sort()
        line_chart = pygal.Line(x_label_rotation=35, width=1000,
        height=532, style=custom_style)
        line_chart.title = project
        line_chart.x_labels = (time_store)
                                                                              
        for i in range(len(data[time_store[0]][project])): 			#WILL ALL PROJECTS HAVE THE SAME METRICS, WILL ONE OF THEM NOT APPEAR?
	    value_store = []
            for time in time_store:
                value_store.append(data[time][project].values()[i])
            metric = data[time][project].keys()[i]
            line_chart.add(metric, value_store)
        
        line_chart.render_in_browser()

def Generate_csv():

    metrics_filter = []
    for project in projects:
        os.chdir(file_dir + '/corpus/' + project)
        with open('solver-statistic.json') as data_file:
            json_keys = json.load(data_file)
	
        for key in json_keys:
            if(key not in metrics_filter):
                metrics_filter.append(key)
    
    height = len(metrics_filter)
    width = len(projects)  
    table = [[' ' for x in range(width+1)] for y in range(height+1)]  
    proj_index = 1
    for project in projects:
        os.chdir(file_dir + '/corpus/' + project)
        with open('solver-statistic.json') as data_file2:
	    json_file = json.load(data_file2)
            
            for project in json_file:
                metrics_index = 1
	        for metrics in metrics_filter: 
	            if(metrics == project):
                        table[metrics_index][proj_index] = json_file[project]
		        break
	            metrics_index += 1
        proj_index += 1

    index_p = 1
    for project in projects:
        table[0][index_p] = project
        index_p += 1
    index_m = 1	   
    for metrics in metrics_filter:
        table[index_m][0] = metrics
        index_m += 1

    os.chdir(file_dir)
    with open('data.csv','w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Execution Time: " + time])
        [writer.writerow(r) for r in table]


Generate_graph(Make_datafile(Run_inference()))
Generate_csv()
