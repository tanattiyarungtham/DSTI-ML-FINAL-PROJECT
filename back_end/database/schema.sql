-- Reference Tables (normalization & consistency)

-- Gender options (e.g., male, female, other)
CREATE TABLE IF NOT EXISTS genders (
    id SERIAL PRIMARY KEY,
    label VARCHAR(50) UNIQUE NOT NULL     -- Ensures each label is unique (e.g., 'female')
);

-- Diet types (e.g., vegetarian, vegan, keto)
CREATE TABLE IF NOT EXISTS diet_types (
    id SERIAL PRIMARY KEY,
    label VARCHAR NOT NULL UNIQUE
);

-- Fitness levels (e.g., beginner, intermediate, advanced)
CREATE TABLE IF NOT EXISTS fitness_levels (
    id SERIAL PRIMARY KEY,
    label VARCHAR NOT NULL UNIQUE
);

-- Possible user goals (e.g., "Lose weight", "Gain muscle")
CREATE TABLE IF NOT EXISTS goals (
    goal_id SERIAL PRIMARY KEY,
    label TEXT NOT NULL UNIQUE
);

-- Main Users Table (normalized version)

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,                    -- Unique user ID
    age INTEGER CHECK(age > 0 AND age < 130),      -- Age constraint (optional safety)
    gender_id INTEGER NOT NULL,                    -- FK to genders table
    height FLOAT CHECK(height > 0),                -- Height must be positive
    weight FLOAT CHECK(weight > 0),                -- Weight must be positive
    target_weight FLOAT CHECK(target_weight > 0),  --target weight in kg
    diet_type_id INTEGER NOT NULL,                 -- FK to diet_types
    fitness_level_id INTEGER NOT NULL,             -- FK to fitness_levels
    FOREIGN KEY (gender_id) REFERENCES genders(id),
    FOREIGN KEY (diet_type_id) REFERENCES diet_types(id),
    FOREIGN KEY (fitness_level_id) REFERENCES fitness_levels(id)
);

-- User ↔ Goals relationship (many-to-many association)

CREATE TABLE IF NOT EXISTS user_goals (
    user_id INTEGER,
    goal_id INTEGER,
    PRIMARY KEY (user_id, goal_id),     -- Prevents duplicates (one user = one goal once)
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
);