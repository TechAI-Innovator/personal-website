import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image

db_path = 'database.db'

def initialize_db():
	"""Creates the database and tables if they do not exist."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	with open('schema.sql', 'r') as f:
		cursor.executescript(f.read())
	
	conn.commit()
	conn.close()

def add_admin(username, password):
	try:
		"""Adds an admin user with a hashed password."""
		conn = sqlite3.connect(db_path)
		cursor = conn.cursor()

		password_hash = generate_password_hash(password)

		cursor.execute('''INSERT INTO admin (username, password)
						VALUES (?, ?)''', (username, password_hash))
		conn.commit()
		return True
	except Exception as e:
		print(f"Error: {e}") 
		return False
	finally:
		conn.close()

def verify_admin(username, password):
	"""Verifies admin login credentials."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute('SELECT password FROM admin WHERE USERNAME = ?',(username,))
	result = cursor.fetchone()

	''' I must check how this result is printed later'''

	conn.close()

	if result and check_password_hash(result[0], password):
		return True
	return False

def add_service(service_name, description):
	"""Adds a new service."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute('''INSERT INTO services (service_name, description)
                    VALUES(?, ?)''', (service_name, description))
	conn.commit()
	conn.close()

def add_project(project_title, service_id, description, tools_used, links):
	try:
		"""Adds a new project under a service"""
		conn = sqlite3.connect(db_path)
		cursor = conn.cursor()

		cursor.execute("""INSERT INTO projects (project_title, service_id, description, tools_used, links)
						VALUES(?,?,?,?,?)""", (project_title, service_id, description, tools_used, links))
		conn.commit()
		return True
	except Exception as e:
		print(f"Error: {e}")
		return False
	finally:
		conn.close()

def add_image(project_id,image_path, category):
	"""Adds a new image_path under a project"""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("""INSERT INTO images (project_id, image_path, category)
			        VALUES(?,?,?)""",(project_id, image_path, category))
	conn.commit()
	conn.close()

def get_services():
	"""Fetches all services."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM services")
	services = cursor.fetchall()
	conn.close()
	return services

def get_service(service_id):
	"""Fetches a particular service."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("""SELECT * FROM services WHERE service_id = ?""", (service_id,))
	service = cursor.fetchone()
	conn.close()
	return service

def get_projects(service_id):
	"""Fetches all projects under a specific service."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM projects WHERE service_id = ?", (service_id,))
	projects = cursor.fetchall()
	conn.close()
	return projects

def get_images(project_id):
	"""Fetches all images for a specific project."""
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("SELECT * from images WHERE project_id = ?", (project_id,))
	images = [{"image_id": img[0], "filename": img[1].split("\\")[1], "category": img[3]} for img in cursor.fetchall()]

	base_image = images[0]["filename"] if images else None

	conn.close()
	return images, base_image


def classify_image(image_path):
    """Classifies an image based on its width."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if width >= 1200:
                return "laptop"
            elif width >= 768:
                return "tablet"
            else:
                return "phone"
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "phone"  # Default category
