DROP TABLE IF EXISTS PostGeo;
DROP TABLE IF EXISTS PostGender;
DROP TABLE IF EXISTS PostDemographics;
DROP TABLE IF EXISTS PostMetric;
DROP TABLE IF EXISTS ContentPost;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'content_type_enum') THEN
    DROP TYPE content_type_enum;
  END IF;
END
$$;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender_enum') THEN
    DROP TYPE gender_enum;
  END IF;
END
$$;
