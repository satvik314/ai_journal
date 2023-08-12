CREATE FUNCTION match_journals (
    query_vec VECTOR (1536),
    match_count INT DEFAULT NULL
) RETURNS TABLE (
    uuid UUID,
    username TEXT,
    date DATE,
    notes TEXT,
    mood_scale INT,
    description TEXT,
    tags TEXT[],
    notes_vec VECTOR (1536),
    similarity FLOAT
)
LANGUAGE plpqsql
AS $$
#variable_conflict use_column
BEGIN 
    RETURN QUERY
    SELECT
        uuid,
        username,
        date,
        notes,
        mood_scale,
        description,
        tags,
        notes_vec,
        1 - (daily_journal.notes_vec <=> query_vec) AS similarity
    FROM daily_journal
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;
