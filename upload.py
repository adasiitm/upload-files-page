from flask import Flask, render_template, request, redirect, send_from_directory, send_file
from flask_uploads import UploadSet, configure_uploads, DATA, url_for
from werkzeug import secure_filename
from time import sleep
import os
import sh
import shutil
import time
import os.path


app = Flask(__name__)

#app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
#app.config['UPLOADED_PHOTOS_DEST'] = 'Uploaded_Files'
app.config['UPLOADED_PHOTOS_DEST'] = '/home/cdhadmin/Lean2.1/docker/Documents'
#app.config['UPLOADED_PHOTOS_DEST'] = '/Users/das/s3uploader'


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'csv', 'doc', 'docx', 'xls', 'xlsx'])
photos = UploadSet('photos')
configure_uploads(app, photos)

@app.route('/', methods=['GET', 'POST'])
def upload():
    
    if request.method == 'POST' and 'photo' in request.files and request.form.get('OptionSelected') == 'OverWrite':
        for f in request.files.getlist('photo'):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            os.chmod(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename), 0o0777)
            dirpath = app.config['UPLOADED_PHOTOS_DEST']
            os.chmod(dirpath, 0o0777)
            msgRet='{} New files uploaded. File with same name overwritten!. '.format((len(request.files.getlist('photo'))))
        #os.system('su -c "/home/cdhadmin/Orchestrator/Data20_Master_v1.sh" cdhadmin')
        #shutil.copyfile(r'/home/cdhadmin/data2_FileUploadUtility/Orchestrator_Trigger.txt', r'/home/cdhadmin/Orchestrator/FilePoller/TriggerDir/Pending/Orchestrator_Trigger.txt')
        return render_template('example.html', msgRet=msgRet)
    elif request.method == 'POST' and request.form.get('OptionSelected') == 'DeleteFiles':
        dirpath = app.config['UPLOADED_PHOTOS_DEST']

        shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        os.chmod(dirpath, 0o0777)

        for f in request.files.getlist('photo'):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            os.chmod(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename), 0o0777)
            text1 = '{} New files uploaded. All old files deleted!.'.format(len(request.files.getlist('photo')))
        #os.system('sh /home/cdhadmin/Orchestrator/Data20_Master_v1.sh')
        #os.system('su -c "/home/cdhadmin/Orchestrator/Data20_Master_v1.sh" cdhadmin')
        #shutil.copyfile(r'/home/cdhadmin/data2_FileUploadUtility/Orchestrator_Trigger.txt', r'/home/cdhadmin/Orchestrator/FilePoller/TriggerDir/Pending/Orchestrator_Trigger.txt')
        return render_template('example.html', text1=str(text1))  
    return render_template('upload.html')


'''@app.route('/example', methods=['POST'])
def next_item():
    if request.method == 'POST':
        import os.path
        import os
        msgRet = "Now inside other function"
    return render_template('example.html', msgRet=msgRet, text1=str(text1))  '''


@app.route('/jobsRun', methods=['GET', 'POST'])
def jobsRun():
    if request.method == 'POST' and request.form.get('example') == 'Start Jobs':
        shutil.copyfile(r'/home/cdhadmin/data2_FileUploadUtility/Orchestrator_Trigger.txt', r'/home/cdhadmin/Orchestrator/FilePoller/TriggerDir/Pending/Orchestrator_Trigger.txt')
        #shutil.copyfile(r'/Users/das/data2.0/data2_FileUploadUtility/Orchestrator_Trigger.txt', r'/Users/das/data2.0/data2_FileUploadUtility/Uploaded_Files/Orchestrator_Trigger.txt')
        #file_path=r'/Users/das/data2.0/data2_FileUploadUtility/Dashboard_Log.log'
        file_path=r'/home/cdhadmin/Orchestrator/Logs/Dashboard_Log.log'
        #os.remove(file_path)
        os.remove(file_path) if os.path.exists(file_path) else None
        while not os.path.exists(file_path):
            time.sleep(2)
        if os.path.isfile(file_path):
            text = open(file_path, 'r+')
            content = text.read()
            text.close()
        return render_template('jobsRun.html', text=content)
    return render_template('example.html')


@app.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'POST':
        #path = r'/Users/das/data2.0/data2_FileUploadUtility/Uploaded_Files'
        # Link to the output files folder
        path = r'/home/cdhadmin/output/'
        def make_tree(path):
            tree = dict(name=path, children=[])
            try: lst = os.listdir(path)
            except OSError as e:
                pass #ignore errors
            else:
                for name in lst:
                    fn = os.path.join(path, name)
                    if os.path.isdir(fn):
                        tree['children'].append(make_tree(fn))
                    else:
                        tree['children'].append(dict(name=fn))
            print(tree)
            return tree
        return render_template('results.html',tree=make_tree(path))
    
    return render_template('jobsRun.html')

@app.route("/download_success", methods=['POST'])
def download_success():
    if request.method == 'POST' and request.form.get('Downloading') == 'Download':
        #folder = r'/Users/das/data2.0/data2_FileUploadUtility/Uploaded_Files'
        #file_name = 'Spark_hadoop_commands.txt'
        # Link to the output.zip
        full_file_name = r'/home/cdhadmin/output.zip'
        #full_file_name = r'/Users/das/data2.0/data2_FileUploadUtility/Uploaded_Files/Spark_hadoop_commands.txt'
        #print("I am inside download")
        #return send_from_directory(folder, file_name, as_attachment=True)
        return send_file(full_file_name, as_attachment=True)
        #return render_template('download_success.html')
    return render_template('results.html')    
    

'''@app.route('/database')
def database():
    # generate some file name
    # save the file in the `database_reports` folder used below
    return render_template('database.html', filename=filename)

@app.route('/database_download/<filename>')
def database_download(filename):
    folder = r'/Users/das/data2.0/data2_FileUploadUtility/Uploaded_Files'
    filename = 'Spark_hadoop_commands.txt'
    return send_from_directory(folder, filename, as_attachment=True)    
'''


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80, debug=True)
