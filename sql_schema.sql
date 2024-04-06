--- Delete database and add again
DROP DATABASE IF EXISTS fake_golf;
CREATE DATABASE fake_golf;
USE fake_golf;

--- Locations Lookup table
--- Stores list of locations
CREATE TABLE locations_lookup (
    id              INT             NOT NULL PRIMARY KEY AUTO_INCREMENT,
    location_name   VARCHAR(25)     NOT NULL,
    modifier_name   VARCHAR(25),
    special         VARCHAR(25),
    icon            VARCHAR(50),
    created_on      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP       NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Status Lookup table
--- Stores status of tournaments
CREATE TABLE tournament_status_lookup (
    id              INT             NOT NULL PRIMARY KEY AUTO_INCREMENT,
    status_name     VARCHAR(50)     NOT NULL,
    description     VARCHAR(500)    NOT NULL,
    error_status    INT             NOT NULL,
    next_status     INT,
    created_on      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP       NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Users table
--- Tracks the information of the players in the game
CREATE TABLE users (
	id 					INT				NOT NULL PRIMARY KEY AUTO_INCREMENT,
    player_name 		VARCHAR(40)		NOT NULL,
    discord_snowflake	VARCHAR(20),
    is_admin 			BOOLEAN			NOT NULL DEFAULT 0,
    is_official 		BOOLEAN			NOT NULL DEFAULT 0,
    created_on 			TIMESTAMP		NOT NULL DEFAULT NOW(),
    updated_on 			TIMESTAMP		NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Courses table
--- Stores data on courses
CREATE TABLE courses (
    id              INT             NOT NULL PRIMARY KEY AUTO_INCREMENT,
    course_name     VARCHAR(100)    NOT NULL,
    designer_id     INT NOT NULL,
    course_image    VARCHAR(500),
    course_url      VARCHAR(500),
    par             INT             NOT NULL,
    yardage         INT             NOT NULL,
    expected_par    DECIMAL(4,2),
    scratch_par     INT,
    created_on      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP       NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Courses Trees table
--- Gives results for shots from trees. Because each course can be different,
---     we store these with courses.id
CREATE TABLE courses_trees (
    id                      INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    course_id               INT         NOT NULL,
    curr_location_id        INT         NOT NULL,
    start_diff              INT         NOT NULL,
    end_diff                INT         NOT NULL,
    new_location_id_par4    INT         NOT NULL,
    new_location_id_par5    INT         NOT NULL,
    created_on              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_on              TIMESTAMP   NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Courses Putting table
--- Gives results for putting. Because each course can be different,
---     we store these with courses.id
CREATE TABLE courses_putting (
    id                  INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    course_id           INT         NOT NULL,
    curr_location_id    INT         NOT NULL,
    start_diff          INT         NOT NULL,
    end_diff            INT         NOT NULL,
    new_location_id     INT         NOT NULL,
    created_on          TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_on          TIMESTAMP   NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Holes table
--- Stores data on individual holes for courses
CREATE TABLE holes (
    id              INT             NOT NULL PRIMARY KEY AUTO_INCREMENT,
    course_id       INT             NOT NULL,
    hole            INT             NOT NULL,
    hole_image      VARCHAR(500),
    hole_url        VARCHAR(500),
    par             INT             NOT NULL,
    yardage         INT             NOT NULL,
    expected_par    DECIMAL(4,2),
    scratch_par     INT,
    created_on      TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP       NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Hole Shots table
--- Stores each hole's shot information.
CREATE TABLE hole_shots (
    id                  INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    hole_id             INT         NOT NULL,
    curr_location_id    INT         NOT NULL,
    start_diff          INT         NOT NULL,
    end_diff            INT         NOT NULL,
    new_location_id     INT         NOT NULL,
    created_on          TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_on          TIMESTAMP   NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Tournaments
--- List of tournaments
CREATE TABLE tournaments (
    id                  INT             NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tournament_name     VARCHAR(100)    NOT NULL,
    designer_id         INT NOT NULL,
    tournament_image    VARCHAR(500),
    description         VARCHAR(500),
    start_time          VARCHAR(25)     NOT NULL,
    end_time            VARCHAR(25)     NOT NULL,
    status_id           INT             NOT NULL,
    created_on          TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_on          TIMESTAMP       NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Tournament Rounds
--- Lists rounds of a tournament
CREATE TABLE tournament_rounds (
    id              INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tournament_id   INT         NOT NULL,
    round           INT         NOT NULL,
    course_id       INT         NOT NULL,
    start_time      VARCHAR(25) NOT NULL,
    end_time        VARCHAR(25) NOT NULL,
    created_on      TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP   NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Tournament Targets
--- Lists target shots for each hole in a tournament round
CREATE TABLE tournament_targets (
    id                      INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    round_id                INT         NOT NULL,
    hole                    INT         NOT NULL,
    shot_1                  INT,
    shot_2                  INT,
    shot_3                  INT,
    shot_4                  INT,
    shot_5                  INT,
    shot_6                  INT,
    shot_7                  INT,
    shot_8                  INT,
    shot_9                  INT,
    created_on              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_on              TIMESTAMP   NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

CREATE TABLE tournament_status (
    id              INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tournament_id   INT         NOT NULL,
    user_id         INT         NOT NULL,
    round           INT         NOT NULL DEFAULT 0,
    hole            INT         NOT NULL DEFAULT 0,
    created_on      TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_on      TIMESTAMP   NOT NULL DEFAULT NOW() ON UPDATE NOW()
);

--- Locations Lookup Values
INSERT INTO locations_lookup (id, location_name, modifier_name, special, icon) VALUES
    (1, "In the hole", NULL, NULL, "hole"),
    (2, "Green", "Close", NULL, "green"),
    (3, "Green", "Short", NULL, "green"),
    (4, "Green", "Average", NULL, "green"),
    (5, "Green", "Medium", NULL, "green"),
    (6, "Green", "Long", NULL, "green"),
    (7, "Green", "Super Long", NULL, "green"),
    (8, "Greenside", "Fairway", NULL, "fairway"),
    (9, "Greenside", "Rough", "rough", "rough"),
    (10, "Greenside", "Bunker", "bunker", "bunker"),
    (11, "Greenside", "Trees", "trees", "trees"),
    (12, "Third", "Fairway", NULL, "fairway"),
    (13, "Third", "Rough", "rough", "rough"),
    (14, "Third", "Bunker", "bunker", "bunker"),
    (15, "Third", "Trees", "trees", "trees"),
    (16, "Second", "Fairway", NULL, "fairway"),
    (17, "Second", "Rough", "rough", "rough"),
    (18, "Second", "Bunker", "bunker", "bunker"),
    (19, "Second", "Trees", "trees", "trees"),
    (20, "Out of Bounds", NULL, "oob", "oob"),
    (21, "Water", NULL, "water", "water"),
    (22, "Tee Box", NULL, NULL, "tee")
;

--- Status Lookup Values
INSERT INTO tournament_status_lookup (id, status_name, description, error_status, next_status) VALUES
    (101, "Starting Tournament Gathering", "The tournament organizer has started giving information about a new tournament.", 10101, 110),
    (110, "Getting Tournament Name", "The tournament organizer is providing the tournament name.", 10110, 120),
    (120, "Getting Tournament Length", "The tournament organizer is providing the number of rounds.", 10120, 121),
    (121, "Getting Round 1 Course", "The tournament organizer is providing the course for the first round.", 10121, 122),
    (122, "Getting Round 2 Course", "The tournament organizer is providing the course for the second round.", 10122, 123),
    (123, "Getting Round 3 Course", "The tournament organizer is providing the course for the third round.", 10123, 124),
    (124, "Getting Round 4 Course", "The tournament organizer is providing the course for the fourth round.", 10124, 125),
    (125, "Getting Round 5 Course", "The tournament organizer is providing the course for the fifth round.", 10125, 126),
    (126, "Getting Round 6 Course", "The tournament organizer is providing the course for the sixth round.", 10126, 127),
    (127, "Getting Round 7 Course", "The tournament organizer is providing the course for the seventh round.", 10127, 128),
    (128, "Getting Round 8 Course", "The tournament organizer is providing the course for the eighth round.", 10128, 129),
    (129, "Getting Round 9 Course", "The tournament organizer is providing the course for the ninth round.", 10129, 150),
    (150, "Waiting for Tournament Sheet Completion", "The tournament organizer is completing the tournament sheet.", 10150, 160),
    (160, "Checking Sheet Information", "The system is checking the validity of the tournament sheet.", 10160, 161),
    (161, "Checking Round 1 Sheet", "The system is checking the validity of the first round sheet.", 10161, 162),
    (162, "Checking Round 2 Sheet", "The system is checking the validity of the second round sheet.", 10162, 163),
    (163, "Checking Round 3 Sheet", "The system is checking the validity of the third round sheet.", 10163, 164),
    (164, "Checking Round 4 Sheet", "The system is checking the validity of the fourth round sheet.", 10164, 165),
    (165, "Checking Round 5 Sheet", "The system is checking the validity of the fifth round sheet.", 10165, 166),
    (166, "Checking Round 6 Sheet", "The system is checking the validity of the sixth round sheet.", 10166, 167),
    (167, "Checking Round 7 Sheet", "The system is checking the validity of the seventh round sheet.", 10167, 168),
    (168, "Checking Round 8 Sheet", "The system is checking the validity of the eighth round sheet.", 10168, 169),
    (169, "Checking Round 9 Sheet", "The system is checking the validity of the ninth round sheet.", 10169, 201),
    
    (201, "Waiting for start of registration", "The tournament is waiting for registration to open.", 10201, 210),
    (210, "Registration Open", "The tournament is open for registration.", 10210, 250),
    (250, "Registration Closed", "The tournament is closed for registration.", 10250, 252),
    (252, "Checking Active Users", "Checking that registered users are in the server.", 10252, 254),
    (254, "Checking Banned Users", "Checking that registered users aren't banned.", 10254, 256),
    (256, "Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10256, 301),

    (301, "Waiting for start of tournament", "The tournament is waiting for the first round to begin.", 10301, 310),
    (310, "Playing Round 1", "The tournament is playing the first round.", 10310, 320),
    (320, "Playing Round 2", "The tournament is playing the  round.", 10320, 330),
    (330, "Playing Round 3", "The tournament is playing the  round.", 10330, 340),
    (340, "Playing Round 4", "The tournament is playing the  round.", 10340, 350),
    (350, "Playing Round 5", "The tournament is playing the  round.", 10350, 360),
    (360, "Playing Round 6", "The tournament is playing the  round.", 10360, 370),
    (370, "Playing Round 7", "The tournament is playing the  round.", 10370, 380),
    (380, "Playing Round 8", "The tournament is playing the  round.", 10380, 390),
    (390, "Playing Round 9", "The tournament is playing the  round.", 10390, 401),

    (401, "Waiting for closing of tournament", "The tournament is waiting to be closed.", 10401, 450),
    (450, "Tournament Completed", "The tournament has been completed.", 10450, NULL),
    (490, "Tournament Canceled", "The tournament was canceled before completion.", 10490, NULL)
;

--- Icon links
--- https://www.flaticon.com/packs/golf-76?word=golf