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
    back_status     INT,
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
    is_banned           BOOLEAN         NOT NULL DEFAULT 0,
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
    shot            INT         NOT NULL DEFAULT 0,
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
INSERT INTO tournament_status_lookup (id, status_name, description, error_status, next_status, back_status) VALUES
    (101, "Starting Tournament Gathering", "The tournament organizer has started giving information about a new tournament.", 10101, 110, NULL),
    (110, "Getting Tournament Name", "The tournament organizer is providing the tournament name.", 10110, 120, 110),
    (120, "Getting Tournament Length", "The tournament organizer is providing the number of rounds.", 10120, 121, 120),
    (121, "Getting Round 1 Course", "The tournament organizer is providing the course for the first round.", 10121, 122, NULL),
    (122, "Getting Round 2 Course", "The tournament organizer is providing the course for the second round.", 10122, 123, NULL),
    (123, "Getting Round 3 Course", "The tournament organizer is providing the course for the third round.", 10123, 124, NULL),
    (124, "Getting Round 4 Course", "The tournament organizer is providing the course for the fourth round.", 10124, 125, NULL),
    (125, "Getting Round 5 Course", "The tournament organizer is providing the course for the fifth round.", 10125, 126, NULL),
    (126, "Getting Round 6 Course", "The tournament organizer is providing the course for the sixth round.", 10126, 127, NULL),
    (127, "Getting Round 7 Course", "The tournament organizer is providing the course for the seventh round.", 10127, 128, NULL),
    (128, "Getting Round 8 Course", "The tournament organizer is providing the course for the eighth round.", 10128, 129, NULL),
    (129, "Getting Round 9 Course", "The tournament organizer is providing the course for the ninth round.", 10129, 150, NULL),
    (150, "Waiting for Tournament Sheet Completion", "The tournament organizer is completing the tournament sheet.", 10150, 160, NULL),
    (160, "Checking Sheet Information", "The system is checking the validity of the tournament sheet.", 10160, 161, 150),
    (161, "Checking Round 1 Sheet", "The system is checking the validity of the first round sheet.", 10161, 162, 150),
    (162, "Checking Round 2 Sheet", "The system is checking the validity of the second round sheet.", 10162, 163, 150),
    (163, "Checking Round 3 Sheet", "The system is checking the validity of the third round sheet.", 10163, 164, 150),
    (164, "Checking Round 4 Sheet", "The system is checking the validity of the fourth round sheet.", 10164, 165, 150),
    (165, "Checking Round 5 Sheet", "The system is checking the validity of the fifth round sheet.", 10165, 166, 150),
    (166, "Checking Round 6 Sheet", "The system is checking the validity of the sixth round sheet.", 10166, 167, 150),
    (167, "Checking Round 7 Sheet", "The system is checking the validity of the seventh round sheet.", 10167, 168, 150),
    (168, "Checking Round 8 Sheet", "The system is checking the validity of the eighth round sheet.", 10168, 169, 150),
    (169, "Checking Round 9 Sheet", "The system is checking the validity of the ninth round sheet.", 10169, 201, 150),
    
    (201, "Waiting for start of registration", "The tournament is waiting for registration to open.", 10201, 210, NULL),
    (210, "Registration Open", "The tournament is open for registration.", 10210, 250, NULL),
    (250, "Registration Closed", "The tournament is closed for registration.", 10250, 252, NULL),
    (252, "Checking Active Users", "Checking that registered users are in the server.", 10252, 254, NULL),
    (254, "Checking Banned Users", "Checking that registered users aren't banned.", 10254, 256, NULL),
    (256, "Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10256, 258, NULL),
    (258, "Checking Player Count", "Checking that there is at least one player in the tournament.", 10258, 300, NULL),

    (300, "Waiting for start of tournament", "The tournament is waiting for Round 1 to begin.", 10300, 302, NULL),
    (302, "Round 1 - Checking Active Users", "Checking that players are in the server.", 10302, 304, NULL),
    (304, "Round 1 - Checking Banned Users", "Checking that players aren't banned.", 10304, 306, NULL),
    (306, "Round 1 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10306, 308, NULL),
    (308, "Round 1 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10308, 310, NULL),
    (310, "Round 1 - Notifying Tournament Organizer", "Notifying the Tournament Organizer the tournament is about to begin.", 10310, 312, NULL),
    (312, "Round 1 - Notifying Players", "Notifying players the tournament is about to begin.", 10312, 320, NULL),
    (320, "Playing Round 1", "The tournament is playing the first round.", 10320, 330, NULL),

    (350, "Waiting for start of tournament", "The tournament is waiting for Round 2 to begin.", 10350, 302, NULL),
    (352, "Round 2 - Checking Active Users", "Checking that players are in the server.", 10352, 304, NULL),
    (354, "Round 2 - Checking Banned Users", "Checking that players aren't banned.", 10354, 306, NULL),
    (356, "Round 2 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10356, 308, NULL),
    (358, "Round 2 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10358, 370, NULL),
    (370, "Playing Round 2", "The tournament is playing the second round.", 10370, 380, NULL),

    (400, "Waiting for start of tournament", "The tournament is waiting for Round 3 to begin.", 10400, 402, NULL),
    (402, "Round 3 - Checking Active Users", "Checking that players are in the server.", 10402, 404, NULL),
    (404, "Round 3 - Checking Banned Users", "Checking that players aren't banned.", 10404, 406, NULL),
    (406, "Round 3 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10406, 408, NULL),
    (408, "Round 3 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10408, 420, NULL),
    (420, "Playing Round 3", "The tournament is playing the third round.", 10420, 430, NULL),

    (450, "Waiting for start of tournament", "The tournament is waiting for Round 4 to begin.", 10450, 402, NULL),
    (452, "Round 4 - Checking Active Users", "Checking that players are in the server.", 10452, 404, NULL),
    (454, "Round 4 - Checking Banned Users", "Checking that players aren't banned.", 10454, 406, NULL),
    (456, "Round 4 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10456, 408, NULL),
    (458, "Round 4 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10458, 420, NULL),
    (470, "Playing Round 4", "The tournament is playing the fourth round.", 10470, 480, NULL),

    (500, "Waiting for start of tournament", "The tournament is waiting for Round 5 to begin.", 10500, 502, NULL),
    (502, "Round 5 - Checking Active Users", "Checking that players are in the server.", 10502, 504, NULL),
    (504, "Round 5 - Checking Banned Users", "Checking that players aren't banned.", 10504, 506, NULL),
    (506, "Round 5 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10506, 508, NULL),
    (508, "Round 5 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10508, 520, NULL),
    (520, "Playing Round 5", "The tournament is playing the fifth round.", 10520, 530, NULL),

    (550, "Waiting for start of tournament", "The tournament is waiting for Round 6 to begin.", 10550, 502, NULL),
    (552, "Round 6 - Checking Active Users", "Checking that players are in the server.", 10552, 504, NULL),
    (554, "Round 6 - Checking Banned Users", "Checking that players aren't banned.", 10554, 506, NULL),
    (556, "Round 6 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10556, 508, NULL),
    (558, "Round 6 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10558, 520, NULL),
    (570, "Playing Round 6", "The tournament is playing the sixth round.", 10570, 580, NULL),

    (600, "Waiting for start of tournament", "The tournament is waiting for Round 7 to begin.", 10600, 602, NULL),
    (602, "Round 7 - Checking Active Users", "Checking that players are in the server.", 10602, 604, NULL),
    (604, "Round 7 - Checking Banned Users", "Checking that players aren't banned.", 10604, 606, NULL),
    (606, "Round 7 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10606, 608, NULL),
    (608, "Round 7 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10608, 620, NULL),
    (620, "Playing Round 7", "The tournament is playing the seventh round.", 10620, 630, NULL),

    (650, "Waiting for start of tournament", "The tournament is waiting for Round 8 to begin.", 10650, 602, NULL),
    (652, "Round 8 - Checking Active Users", "Checking that players are in the server.", 10652, 604, NULL),
    (654, "Round 8 - Checking Banned Users", "Checking that players aren't banned.", 10654, 606, NULL),
    (656, "Round 8 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10656, 608, NULL),
    (658, "Round 8 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10658, 620, NULL),
    (670, "Playing Round 8", "The tournament is playing the eighth round.", 10670, 680, NULL),

    (700, "Waiting for start of tournament", "The tournament is waiting for Round 9 to begin.", 10700, 702, NULL),
    (702, "Round 9 - Checking Active Users", "Checking that players are in the server.", 10702, 704, NULL),
    (704, "Round 9 - Checking Banned Users", "Checking that players aren't banned.", 10704, 706, NULL),
    (706, "Round 9 - Checking Non-Playing Users", "Checking that registered users aren't playing in another tournament.", 10706, 708, NULL),
    (708, "Round 9 - Checking Player Count", "Checking that there is at least one player in the tournament.", 10708, 720, NULL),
    (720, "Playing Round 9", "The tournament is playing the ninth round.", 10720, 730, NULL),

    (801, "Waiting for closing of tournament", "The tournament is waiting to be closed.", 10801, 850, NULL),
    (850, "Tournament Completed", "The tournament has been completed.", 10850, NULL, NULL),
    (890, "Tournament Canceled", "The tournament was canceled before completion.", 10890, NULL, NULL)
;

--- Icon links
--- https://www.flaticon.com/packs/golf-76?word=golf