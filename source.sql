CREATE TABLE users (
    id SERIAL PRIMARY KEY,
	firstname VARCHAR(50),
	lastname VARCHAR(50),
    username VARCHAR(50),
    email VARCHAR(150),
    password VARCHAR(250),
    avatar VARCHAR(250),
	date_created VARCHAR(50)
);

CREATE TABLE deck(
    user_id INT REFERENCES users(id),
    pokemon JSON 
);