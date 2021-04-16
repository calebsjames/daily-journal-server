INSERT INTO `entries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`date`	12/12/20,
	`concept`	"Things",
    `text`  "Stuff",
    `moodId` 1,
    
);

INSERT INTO `entries` VALUES (null, "12/12/20", "Kennel", "Boxer", 1);


CREATE TABLE `moods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`mood` TEXT NOT NULL

);