CREATE TABLE IF NOT EXISTS 'tblBlogPosts' (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"date"	TEXT,
	"title"	TEXT,
	"message"	TEXT,
	"image"	TEXT
)


CREATE TABLE IF NOT EXISTS 'tblBenefits' (
  "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"title"	TEXT,
	"message"	TEXT,
	"image"	TEXT
)


CREATE TABLE IF NOT EXISTS 'tblContact' (
  "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"firstname"	TEXT,
	"lastname"	TEXT,
	"jobtitle"	TEXT,
	"companytitle"	TEXT,
	"companydesription"	TEXT,
	"workemail"	TEXT,
	"phonenumber"	INTEGER,
	"message"	TEXT
)
