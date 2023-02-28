CREATE SCHEMA IF NOT EXISTS content;

CREATE TYPE content.type AS ENUM ('movie', 'tv_show', 'series', 'cartoons');

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type content.type not null,
    created timestamp with time zone default current_timestamp,
    modified timestamp with time zone default current_timestamp
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone default current_timestamp,
    modified timestamp with time zone default current_timestamp,
    UNIQUE(name)
); 

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
	CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) REFERENCES content.genre(id),
    film_work_id uuid NOT NULL,
	CONSTRAINT fk_film_work_id FOREIGN KEY (film_work_id) REFERENCES content.film_work(id),
    created timestamp with time zone default current_timestamp,
    modified timestamp with time zone default current_timestamp
); 

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone default current_timestamp,
    modified timestamp with time zone default current_timestamp,
    UNIQUE(full_name)
); 

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
	CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES content.person(id),
    film_work_id uuid NOT NULL,
	CONSTRAINT fk_film_work_id FOREIGN KEY (film_work_id) REFERENCES content.film_work(id),
    role TEXT NOT NULL,
    created timestamp with time zone default current_timestamp,
    modified timestamp with time zone default current_timestamp
); 

CREATE UNIQUE INDEX IF NOT EXISTS film_work_title_date ON content.film_work (title, creation_date);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_type_rating_date ON content.film_work (type, rating, creation_date);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

-- CREATE TYPE gender AS ENUM ('male', 'female');
-- ALTER TABLE content.person ADD COLUMN "gender" gender NULL;
COMMIT; 
