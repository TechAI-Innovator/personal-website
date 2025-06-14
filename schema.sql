CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_title TEXT NOT NULL,
    service_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    tools_used TEXT NOT NULL,
    links TEXT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services (service_id)
);

CREATE TABLE IF NOT EXISTS images (
	image_id INTEGER PRIMARY KEY AUTOINCREMENT,
	image_path TEXT NOT NULL,
	project_id INTEGER NOT NULL,
    category TEXT NOT NULL,
	FOREIGN KEY (project_id) REFERENCES projects (project_id)
);

CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- INSERT INTO admin (username, password) VALUES('MHans', 'scrypt:32768:8:1$3cABYv7NxkCuIa6P$298568b6221f866e6b7882819c9f9a8c2925fbb494651d18d3c9d25af3a623ffbd63b6cba87b2815dd9664fbf58ea13128c081b70afa8e96cbd3b4bd8f2e422b');
-- truncate table images;

