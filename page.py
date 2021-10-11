import os
from flask import Flask, render_template, request, send_file, Response
from werkzeug.utils import secure_filename
from db import db, db_init
from models import File

app = Flask (__name__)

#UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/upload')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

#Página inicial
@app.route("/")
def home():
	return render_template("index.html")

#Página admin (adicionar nova imagem)
@app.route("/admin")
def admin():
	return render_template("add.html")

#Método para adicionar imagem do computador no banco de dados
@app.route('/upload', methods = ['POST'])
def upload():
	file = request.files['imagem']
	#savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
	#file.save(savePath)
	filename = secure_filename(file.filename)
	mimetype = file.mimetype
	img = File(img = file.read(), name = filename, mimetype = mimetype)
	db.session.add(img)
	db.session.commit()
	return 'Upload da imagem ' + file.filename  + ' realizado com sucesso!', 200

#Método que retorna a imagem do banco de dados com base no id
@app.route('/<int:id>')
def get_img(id):
	img = File.query.filter_by(id = id).first()
	if not img:
		return 'Img Not Found!', 404
	return Response(img.img, mimetype = img.mimetype)

if __name__ == '__main__':
	app.run(debug = True)


