from flask import Flask, render_template, request, redirect
from flask_uploads import UploadSet, configure_uploads, DATA, url_for
from werkzeug import secure_filename
import os
import sh
import shutil


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
            msgRet='{} New files uploaded. File with same name overwritten. '.format((len(request.files.getlist('photo'))))
        #os.system('su -c "/home/cdhadmin/Orchestrator/Data20_Master_v1.sh" cdhadmin')
        shutil.copyfile(r'/home/cdhadmin/data2_FileUploadUtility/Orchestrator_Trigger.txt', r'/home/cdhadmin/Orchestrator/FilePoller/TriggerDir/Pending/Orchestrator_Trigger.txt')
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
            text1 = '{} New files uploaded. All old files deleted.'.format(len(request.files.getlist('photo')))
        #os.system('sh /home/cdhadmin/Orchestrator/Data20_Master_v1.sh')
        #os.system('su -c "/home/cdhadmin/Orchestrator/Data20_Master_v1.sh" cdhadmin')
        shutil.copyfile(r'/home/cdhadmin/data2_FileUploadUtility/Orchestrator_Trigger.txt', r'/home/cdhadmin/Orchestrator/FilePoller/TriggerDir/Pending/Orchestrator_Trigger.txt')
        return render_template('example.html', text1=str(text1))  
    return render_template('upload.html')


@app.route('/example', methods=['POST'])
def delete_item():
    import os.path
    import os
    #directory='/path/to/dir'
    #os.chdir(app.config['UPLOADED_PHOTOS_DEST
    dirpath = app.config['UPLOADED_PHOTOS_DEST']

    shutil.rmtree(dirpath)
    os.mkdir(dirpath)
    #msgRet = (app.config['UPLOADED_PHOTOS_DEST'])
    msgRet = "Now inside other function"
    selectedOption = request.form.get('OptionSelected')
    return render_template('example.html', msgRet=msgRet, text1=str(text1))  

@app.route("/test" , methods=['POST', 'GET'])
def test():
    text = request.form.get('OptionSelected')
    return(str(text))

      

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80, debug=False)
