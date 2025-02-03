-- Drop tables if they already exist (to avoid conflicts during recreation)
IF OBJECT_ID('Users', 'U') IS NOT NULL DROP TABLE Users;
IF OBJECT_ID('Athletes', 'U') IS NOT NULL DROP TABLE Athletes;
IF OBJECT_ID('TrainingPlans', 'U') IS NOT NULL DROP TABLE TrainingPlans;
IF OBJECT_ID('PrivateCoaching', 'U') IS NOT NULL DROP TABLE PrivateCoaching;
IF OBJECT_ID('Competitions', 'U') IS NOT NULL DROP TABLE Competitions;
IF OBJECT_ID('CompetitionAthletes', 'U') IS NOT NULL DROP TABLE CompetitionAthletes;
IF OBJECT_ID('WeightCategories', 'U') IS NOT NULL DROP TABLE WeightCategories;

-- Create the Users table
CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the TrainingPlans table
CREATE TABLE TrainingPlans (
    plan_name VARCHAR(100) PRIMARY KEY,
    weekly_fee DECIMAL(10,2) NOT NULL
);

-- Create the WeightCategories table
CREATE TABLE WeightCategories (
    category_name VARCHAR(50) PRIMARY KEY,
    upper_weight_limit DECIMAL(10,2) NOT NULL
);

-- Create the Athletes table
CREATE TABLE Athletes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    training_plan VARCHAR(100) NOT NULL,
    current_weight DECIMAL(10,2) NOT NULL,
    competition_weight_category VARCHAR(50),
    FOREIGN KEY (training_plan) REFERENCES TrainingPlans(plan_name),
    FOREIGN KEY (competition_weight_category) REFERENCES WeightCategories(category_name)
);

-- Create the Competitions table
CREATE TABLE Competitions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    entry_fee DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL
);

-- Create the CompetitionAthletes table (many-to-many relationship between Competitions and Athletes)
CREATE TABLE CompetitionAthletes (
    competition_id INT NOT NULL,
    athlete_id INT NOT NULL,
    PRIMARY KEY (competition_id, athlete_id),
    FOREIGN KEY (competition_id) REFERENCES Competitions(id),
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id)
);

-- Create the PrivateCoaching table
CREATE TABLE PrivateCoaching (
    athlete_id INT NOT NULL,
    coaching_hours INT NOT NULL,
    FOREIGN KEY (athlete_id) REFERENCES Athletes(id)
);

-- Insert sample data into WeightCategories
INSERT INTO WeightCategories (category_name, upper_weight_limit) VALUES
('Heavyweight', 10000.00),
('Light-Heavyweight', 100.00),
('Middleweight', 90.00),
('Light-Middleweight', 81.00),
('Lightweight', 73.00),
('Flyweight', 66.00);

-- Insert sample data into TrainingPlans
INSERT INTO TrainingPlans (plan_name, weekly_fee) VALUES
('Beginner', 10.00),
('Intermediate', 15.00),
('Advanced', 20.00);