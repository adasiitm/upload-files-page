Usage:

pip install -r requirements.txt

cd data2_FileUploadUtility
sudo /etc/init.d/apache2 stop
sudo ~/miniconda3/bin/python upload.py
Normally this may work in systems where sudo & non-sudo users have same python path
sudo python upload.py

If any issues installing python packages, please install following python modules:
pip install flask
pip install flask_uploads
pip install sh
pip install shutil
