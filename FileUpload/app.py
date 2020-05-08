import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
app = Flask(__name__,template_folder =  "templates")

if not os.path.exists('uploads'):
    os.makedirs('uploads')

UPLOAD_FOLDER = 'uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/",methods=["POST","GET"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            print("No File")
            return render_template('failure.html')
            #return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No File')
            return render_template('failure.html')
            #return redirect(request.url)

        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print("Saved")
            #return render_template('failure.html')
            return redirect('download/'+filename)

    return render_template('upload.html')

@app.route('/download/<filename>',methods = ["GET"])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/report-generate/<filename>')
def return_files(filename):
    #file_path = UPLOAD_FOLDER + filename
    #return send_file(file_path,as_attachment=True,attachment_filename='')

    file_path = "/home/shivansh/Downloads/Trivy-App/FileUpload/uploads/" + filename
    #session = subprocess.Popen(['trivy --input '+file_path], stdout=PIPE, stderr=PIPE, shell=True)
    #stdout, stderr = session.communicate()
    
    report = subprocess.run(['trivy' ,'--input', file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print(report.stdout.decode(utf))
    #print(report.stdout)
    return '<pre>'+report.stdout.decode()+'</pre>'



if __name__ == "__main__":
    app.run(debug=True)
