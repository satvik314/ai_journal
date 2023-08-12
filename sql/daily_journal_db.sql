create extension if not exists "uuid-ossp";

create table
  daily_journal (
    id bigint primary key generated always as identity,
    uuid uuid default uuid_generate_v4 (),
    created_at timestamp with time zone default timezone ('utc'::text, now()) not null,
    username text,
    date date,
    notes text,
    mood_scale int,
    description text,
    tags text[],
    notes_vec VECTOR (1536)
  );