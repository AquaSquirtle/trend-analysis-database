  CREATE TABLE IF NOT EXISTS PostingSchedule (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES Company(id) ON DELETE CASCADE,
    best_day VARCHAR,
    best_time TIME,
    effectiveness_score FLOAT
  );

  CREATE TABLE IF NOT EXISTS ContentTypeAnalysis (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES Company(id) ON DELETE CASCADE,
    content_type VARCHAR,
    engagement_rate FLOAT
  );
