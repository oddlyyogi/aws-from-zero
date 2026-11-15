CREATE TABLE notes (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title      text NOT NULL CHECK (title <> ''),
  body       text NOT NULL DEFAULT '',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE photos (
  note_id bigint NOT NULL REFERENCES notes (id) ON DELETE CASCADE,
  s3_key  text   NOT NULL,
  PRIMARY KEY (note_id, s3_key)
);
