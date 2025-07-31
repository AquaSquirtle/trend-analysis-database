DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'content_type_enum') THEN
    CREATE TYPE content_type_enum AS ENUM ('text', 'image', 'video');
  END IF;
END
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender_enum') THEN
    CREATE TYPE gender_enum AS ENUM ('male', 'female', 'other');
  END IF;
END
$$;


CREATE TABLE IF NOT EXISTS ContentPost (
  id SERIAL PRIMARY KEY,
  company_id INTEGER NOT NULL REFERENCES Company(id) ON DELETE CASCADE,
  social_id INTEGER NOT NULL REFERENCES SocialNetwork(id),
  external_id VARCHAR,
  content_type content_type_enum NOT NULL,
  text_content TEXT,
  publish_date TIMESTAMP,
  url VARCHAR
);

CREATE TABLE IF NOT EXISTS PostMetric (
  id SERIAL PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES ContentPost(id) ON DELETE CASCADE,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS PostDemographics (
  id SERIAL PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES ContentPost(id) ON DELETE CASCADE,
  age_group VARCHAR NOT NULL,
  value FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS PostGender (
  id SERIAL PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES ContentPost(id) ON DELETE CASCADE,
  gender gender_enum NOT NULL,
  value FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS PostGeo (
  id SERIAL PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES ContentPost(id) ON DELETE CASCADE,
  region VARCHAR NOT NULL,
  value FLOAT NOT NULL
);
