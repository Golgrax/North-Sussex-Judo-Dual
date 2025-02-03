CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Athletes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    training_plan TEXT NOT NULL,
    current_weight REAL NOT NULL,
    competition_weight_category TEXT,
    FOREIGN KEY (training_plan) REFERENCES TrainingPlans(plan_name)
);

CREATE TABLE TrainingPlans (
    plan_name TEXT PRIMARY KEY,
    weekly_fee REAL NOT NULL
);

CREATE TABLE PrivateCoaching (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER NOT NULL,
    coaching_hours REAL NOT NULL,
        FOREIGN KEY (athlete_id) REFERENCES Athletes(id)
);

CREATE TABLE Competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_name TEXT NOT NULL,
    entry_fee REAL NOT NULL,
    date TEXT NOT NULL
);

CREATE TABLE CompetitionAthletes (
    competition_id INTEGER NOT NULL,
    athlete_id INTEGER NOT NULL,
    FOREIGN KEY (competition_id) REFERENCES Competitions(id),
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id),
    PRIMARY KEY (competition_id, athlete_id)
);

CREATE TABLE WeightCategories(
    category_name TEXT PRIMARY KEY,
    upper_weight_limit REAL NOT NULL
);

INSERT INTO WeightCategories (category_name, upper_weight_limit) VALUES
('Heavyweight', 10000),
('Light-Heavyweight', 100),
('Middleweight', 90),
('Light-Middleweight', 81),
('Lightweight', 73),
('Flyweight', 66);