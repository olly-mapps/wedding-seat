'''
Flask Framework
'''

from app import app
from app import model 
from app import scripts
from app import forms
from flask import request, render_template, url_for, redirect, session
import json 
import ast
import csv
from werkzeug.utils import secure_filename
from datetime import datetime
import os

'''
CSV Validation
'''
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app.secret_key = 'key'

'''
View to input problem parameters
'''

@app.route("/", methods=['GET', 'POST'])
def index():
    form = forms.InputForm()
    if form.validate_on_submit():
        param = form.data
        return redirect(url_for('name_input', param = param))
    return render_template('param_input.html', title = "input", form=form)

'''
View to guest input names
'''

@app.route("/name_input<param>", methods = ['GET', 'POST'])
def name_input(param):
    param = ast.literal_eval(param)
    guest_count = param["guest_count"]
    child_count = param["child_count"]
    if request.method == "POST":
        guest_list = request.form.to_dict()
        guest_list.popitem()
        bride = guest_list.pop('Bride')
        groom = guest_list.pop('Groom')
        names = list(guest_list.values())
        names.insert(0, groom + " (Groom)")
        names.insert(0, bride + " (Bride)")
        names.extend([("Child " + str(child+1)) for child in range(child_count)])
        session["names"] = names
        return redirect(url_for('relationship_matrix', param = param))
    return render_template('name_input.html', guest_count = guest_count)

'''
View to input or upload relationship matrix
'''

@app.route("/relationship_matrix<param>", methods=['GET', 'POST'])
def relationship_matrix(param):

    use_param = ast.literal_eval(param)
    names = session.get("names")
    guest_count = use_param["guest_count"]

    '''
    CSV Input
    '''

    if request.method == "POST":
        csv_input = request.files.get('csvfile')
        if csv_input and allowed_file(csv_input.filename):
            filename = secure_filename(csv_input.filename)
            save_location = os.path.join(r'app/tmp', filename)
            csv_input.save(save_location)

            csv_list_and_names = scripts.process_csv(save_location)

            np_input = csv_list_and_names[0]
            names = csv_list_and_names[1]

            session["np_input"] = np_input
            session["names"] = names

            return redirect(url_for('run_model', use_param = use_param))

        elif not request.form.to_dict() and not allowed_file(csv_input.filename):
            return redirect(url_for('relationship_matrix', param = use_param))


        '''
        Manual Input Array
        '''

        dict_input = request.form.to_dict()
        np_input = scripts.to_relationship_matrix(dict_input)
        session["np_input"] = np_input

        return redirect(url_for('run_model', use_param = use_param))

    return render_template('table.html', names = names[:guest_count])

'''
General test view (outputs whatever is passed to it)
'''

@app.route("/test_2<use_param>", methods = ['GET', 'POST'])
def test_2(use_param):
    #return render_template('results.html', content = table)
    table_list = session.get('table_list')
    return table_list

'''
View to run model
'''

@app.route("/run_model<use_param>", methods=["GET", "POST"])
def run_model(use_param):
    use_param_2 = ast.literal_eval(use_param)
    use_np_input = session.get("np_input", None)
    result_raw = model.run_model(use_param_2, use_np_input)
    session["result_raw"] = result_raw
    return redirect(url_for('display_result', use_param_2 = use_param_2)) 
    return result_raw

'''
View to display the result
'''

@app.route("/display_result<use_param_2>")
def display_result(use_param_2): 
    use_param_2 = ast.literal_eval(use_param_2)
    guest_count = use_param_2["guest_count"]
    use_result_raw = session.get('result_raw', None)
    names = session.get("names", None)
    
    table_list = scripts.display_model(use_result_raw, names)
    session["table_list"] = table_list
    #return redirect(url_for('test_2', use_param = use_param_2))
    return render_template('result.html', table_list = table_list)

