CREATE TABLE IF NOT EXISTS logs (

    unique_id INTEGER PRIMARY KEY AUTOINCREMENT,

    input TEXT NOT NULL,

    cleaned_input TEXT,

    status TEXT NOT NULL,

    error TEXT,

    post_id TEXT,

    title TEXT,

    raw_response TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    request_id TEXT,

    ai_generated TEXT,

    ai_explanation TEXT

);


CREATE TABLE IF NOT EXISTS trace (

    trace_id INTEGER PRIMARY KEY,

    status TEXT,

    request_id TEXT,

    step_name TEXT,

    step_order INTEGER,

    error TEXT,

    workflow_attempts INTEGER,


    UNIQUE(request_id, step_name, step_order)

);



CREATE TABLE IF NOT EXISTS attempts (

    id INTEGER PRIMARY KEY,

    trace_id INTEGER,

    step_name TEXT,

    attempt INTEGER,

    status TEXT,

    error TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(trace_id)

        REFERENCES trace(trace_id)

);
