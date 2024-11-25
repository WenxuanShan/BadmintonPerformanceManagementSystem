#Edit Database
import sqlite3
from sqlite3 import Error

###Using SQL
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


###Database
#Create tables: organizations, users, players, matches.
def createTables(database):
    create_organizations_table = """
    CREATE TABLE IF NOT EXISTS organizations (
        organizationID INTEGER PRIMARY KEY AUTOINCREMENT,
        organizationName TEXT
        );
        """
    execute_query(create_connection(database), create_organizations_table)
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        firstName TEXT,
        lastName TEXT,
        organizationID INTEGER,
        username TEXT,
        password TEXT,
        email TEXT,
        identity TEXT,
        FOREIGN KEY (organizationID) REFERENCES organizations(organizationID)
        );
        """
    execute_query(create_connection(database), create_users_table)
    create_players_table = """
    CREATE TABLE IF NOT EXISTS players (
        userID INTEGER,
        firstName TEXT,
        lastName TEXT,
        yearGroup INTEGER,
        gender TEXT,
        dominantHand TEXT,
        scoreTotal INTEGER,
        scoreAve INTEGER,
        matchTotal INTEGER,
        wonTotal INTEGER,
        foreHand INTEGER,
        backHand INTEGER,
        highShots INTEGER,
        lowShots INTEGER,
        foreCourt INTEGER,
        midCourt INTEGER,
        backCourt INTEGER,
        leftCourt INTEGER,
        rightCourt INTEGER,
        miss INTEGER,
        failure INTEGER,
        foul INTEGER,
        FOREIGN KEY (userID) REFERENCES users(userID)
        );
        """
    execute_query(create_connection(database), create_players_table)
    create_matches_table = """
    CREATE TABLE IF NOT EXISTS matches (
        matchID INTEGER PRIMARY KEY AUTOINCREMENT,
        organizationID INTEGER,
        name TEXT,
        matchDate DATE,
        vedioLink TEXT,
        player1ID TEXT,
        player2ID TEXT,
        player1Score INTEGER,
        player2Score INTEGER,
        FOREIGN KEY (organizationID) REFERENCES players(organizationID),
        FOREIGN KEY (player1ID) REFERENCES players(userID),
        FOREIGN KEY (player2ID) REFERENCES players(userID)
        );
        """
    execute_query(create_connection(database), create_matches_table)

#Create a trigger for automatically insert into players table when inserted into users table.
def createTrigger(database):
    create_players = """
    CREATE TRIGGER insert_players
    AFTER INSERT ON users
    FOR EACH ROW 
    BEGIN
        INSERT INTO players (userID,firstName,lastName,gender,dominantHand,scoreTotal,scoreAve,matchTotal,wonTotal,foreHand,backHand,highShots,lowShots,foreCourt,midCourt,backCourt,leftCourt,rightCourt,miss,failure,foul)
        VALUES (NEW.userID, NEW.firstName, NEW.lastName,'male/female/other','left/right',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
    END;
    """
    execute_query(create_connection(database), create_players)
    update_players = """
    CREATE TRIGGER update_players
    AFTER INSERT ON matches
    FOR EACH ROW
    BEGIN
        UPDATE players
        SET scoreTotal = 
                CASE 
                    WHEN players.userID = NEW.player1ID THEN scoreTotal + NEW.player1Score
                    WHEN players.userID = NEW.player2ID THEN scoreTotal + NEW.player2Score
                    ELSE scoreTotal
                END,
            scoreAve = 
                CASE 
                    WHEN players.userID = NEW.player1ID THEN (scoreTotal + NEW.player1Score) / (matchTotal + 1)
                    WHEN players.userID = NEW.player2ID THEN (scoreTotal + NEW.player2Score) / (matchTotal + 1)
                    ELSE scoreAve
                END,
            matchTotal = 
                CASE 
                    WHEN players.userID = NEW.player1ID OR players.userID = NEW.player2ID THEN matchTotal + 1
                    ELSE matchTotal
                END,
            wonTotal = 
                CASE 
                    WHEN players.userID = NEW.player1ID AND NEW.player1Score > NEW.player2Score THEN wonTotal + 1
                    WHEN players.userID = NEW.player1ID AND NEW.player2Score > NEW.player1Score THEN wonTotal + 1
                    ELSE wonTotal
                END
        WHERE players.userID = NEW.player1ID OR players.userID = NEW.player2ID;
    END;
    """
    execute_query(create_connection(database), update_players)

#Create test organizations.
def createOrganization(database):
    create_organizations = """
    INSERT INTO
    organizations (organizationID,organizationName)
    VALUES
        (1,'organization1'),
        (2,'organization2');
        """
    execute_query(create_connection(database), create_organizations)

#Create test users.
def createUser(database):
    create_users = """
    INSERT INTO
    users (userID, title, firstName, lastName, organizationID, username, password, email, identity)
    VALUES
        ('001','Miss', 'Amy', 'Z', '1','user1','password1','az@gmail.com','organizer'),
        ('002','Mr', 'Ben', 'Y', '1','user2','password2','by@gmail.com','player'),
        ('003','Miss', 'Chloe', 'X', '1','user3','password3','cx@gmail.com','player'),
        ('004','Mr', 'David', 'V', '2','user4','password4','cx@gmail.com','player'),
        ('005','Miss', 'Emma', 'W', '1','user5','password5','ew@gmail.com','player'),
        ('006','Miss', 'Fed', 'V', '2','user6','password6','fv@gmail.com','organizer'),
        ('007','Mr', 'Grant', 'U', '2','user7','password7','gu@gmail.com','player'),
        ('008','Miss', 'Harriet', 'T', '2','user8','password8','ht@gmail.com','player');
        """
    execute_query(create_connection(database), create_users)

#Create a trigger for automatically update players table after a match is recorded.
#Create test matches.
#Initialize the players table relating to the test matches created.
def createMatches(database):
    create_matches = """
    INSERT INTO
    matches (matchID,organizationID,name,matchDate,vedioLink,player1ID,player2ID,player1Score,player2Score)
    VALUES
        ('001','1','match1','2021-09-01','link1','2','3','21','8'),
        ('002','2','match2','2022-09-01','link2','4','6','16','21'),
        ('003','1','match3','2021-07-03','link3','2','3','16','21');
        """
    execute_query(create_connection(database),create_matches)
    initialize_players = """
    UPDATE players
    SET foreHand = 23,
        backHand = 14,
        highShots = 24,
        lowShots = 8,
        foreCourt = 11,
        midCourt = 12,
        backCourt = 21,
        leftCourt = 26,
        rightCourt = 11,
        miss = 5,
        failure = 0,
        foul = 0
        WHERE userID = '2';
        """
    execute_query(create_connection(database),initialize_players)
    initialize_players = """
    UPDATE players
    SET foreHand = 18,
        backHand = 11,
        highShots = 20,
        lowShots = 9,
        foreCourt = 6,
        midCourt = 9,
        backCourt = 14,
        leftCourt = 10,
        rightCourt = 14,
        miss = 17,
        failure = 2,
        foul = 2
        WHERE userID = '3';
        """
    execute_query(create_connection(database),initialize_players)
    initialize_players = """
    UPDATE players
    SET foreHand = 12,
        backHand = 4,
        highShots = 10,
        lowShots = 6,
        foreCourt = 3,
        midCourt = 5,
        backCourt = 8,
        leftCourt = 5,
        rightCourt = 11,
        miss = 5,
        failure = 0,
        foul = 0
        WHERE userID = '4';
        """
    execute_query(create_connection(database),initialize_players)
    initialize_players = """
    UPDATE players
    SET foreHand = 14,
        backHand = 7,
        highShots = 17,
        lowShots = 4,
        foreCourt = 5,
        midCourt = 7,
        backCourt = 10,
        leftCourt = 8,
        rightCourt = 13,
        miss = 0,
        failure = 0,
        foul = 0
        WHERE userID = '6';
        """
    execute_query(create_connection(database),initialize_players)

##Create the tables first
createTables('bpmsdatabase')
##Create test organizations
createOrganization('bpmsdatabase')
##Create the insert_players trigger
createTrigger('bpmsdatabase')
##Create test users
createUser('bpmsdatabase')
##Create the update_players trigger and test matches
createMatches('bpmsdatabase')
