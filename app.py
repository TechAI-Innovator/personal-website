from flask import Flask, render_template, request, redirect, url_for, flash, session
from engine import (initialize_db,
                    add_admin, verify_admin, 
                    add_service, add_project, 
                    add_image, get_services, 
                    get_projects, get_images, 
                    get_service, classify_image)
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

initialize_db()

@app.route('/')
def index():
    return redirect('/index')

@app.route('/index')
def index1():
    services = get_services()
    return render_template('index.html', services = services)

@app.route('/services-<int:service_id>')
def service_page(service_id):
    service = get_service(service_id)
    projects = get_projects(service_id)
    project_images = {}

    for project in projects:
        _, base_image = get_images(project[0])
        project_images[project[0]] = base_image

    return render_template('service_page.html',
                           projects = projects,
                           project_images=project_images,
                           service = service)

@app.route('/services-<int:service_id>/projects-<int:project_id>')
def project_page(project_id, service_id):
    images_db, base_image = get_images(project_id)
    print(images_db)


    return render_template('image_display.html', 
                           images = images_db, 
                           base_image=base_image)







# Admin Routes
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_admin(username, password):
            session['admin'] = username
            return redirect('/admin/dashboard')
        else:
            flash('Invalid credentials', 'danger')
    return render_template("admin_login.html")

@app.route('/admin/register', methods = ['GET', 'POST'])
def admin_register():
    register = "Register"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if add_admin(username, password):
            return redirect("/admin")
        else:
            flash("password already exists", "danger")
            return redirect("/admin/register")
    return render_template("admin_login.html", register = register)


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin')
    services = get_services()
    projects = []

    if services:
        for service in services:
            projects+=get_projects(service[0])

    return render_template('admin_dashboard.html', 
                           services = services, 
                           projects = projects if projects else[]) 

@app.route('/admin/logout')
def admin_logout():
	session.pop('admin', None)
	return redirect('/admin')

@app.route('/admin/add-service', methods = ['POST'])
def admin_add_service():
    if 'admin' not in session:
        return redirect('/admin')

    service_name = request.form['service_name']
    description = request.form['description']
    
    add_service(service_name, description)
    return redirect('/admin/dashboard')

@app.route('/admin/add-project', methods = ['POST'])
def admin_add_project():
    if 'admin' not in session:
         return redirect('/admin')
    
    service_id = request.form['service_id']
    project_title = request.form['project_title']
    description = request.form['description']
    tools_used = request.form['tools_used']
    links = request.form['links']


    if add_project(project_title, service_id, description, tools_used, links):
        return redirect('/admin/dashboard')
    else:
         flash('Error adding project', 'danger')
         return redirect('/admin/dashboard')

@app.route("/admin/upload-image", methods=['POST'])
def upload_image():
    if 'admin' not in session:
        return redirect('/admin')
    
    project_id = request.form['project_id']

    if 'image' not in request.files:
        flash('No file path', 'danger')
        return redirect('/admin/dashboard')

    file = request.files['image']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect('/admin/dashboard')
      
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Classify the image based on size
    category = classify_image(file_path)

    # Store image path and category in the database
    add_image(project_id, file_path, category)

    flash('Image uploaded successfully', 'success')
    return redirect('/admin/dashboard')
    

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')