import pymysql

from discord.ext import commands

import keys

CONNECTION = pymysql.connect(
    host = keys.db_host,
    user = keys.db_user,
    password = keys.db_password,
    database = keys.db_database,
    autocommit = True,
    cursorclass = pymysql.cursors.DictCursor
)

##### DATABASE QUERIES ########################################################
def db_create(q, v):
    cur = CONNECTION.cursor()
    cur.execute(q, v)
    response = cur.lastrowid
    cur.close()

    return response

def db_read(q, v=None):
    cur = CONNECTION.cursor()
    if v is not None:
        cur.execute(q, v)
    else:
        cur.execute(q)
    response = cur.fetchall()
    cur.close()

    return response

def db_update(q, v):
    cur = CONNECTION.cursor()
    cur.execute(q, v)
    response = cur.rowcount
    cur.close()

    return response

def db_delete(q, v):
    cur = CONNECTION.cursor()
    cur.execute(q, v)
    response = cur.rowcount
    cur.close()

    return response
###############################################################################

##### CHECK QUERIES ###########################################################
##### Read ####################################################################
def get_round_info(tid, round):
    """Gets information of given round for given tournament."""
    query = '''
        SELECT *
        FROM tournament_rounds tr
        WHERE tournament_id = %s AND round = %s;
    '''
    variables = (tid, round)
    response = db_read(query, variables)

    return response

def get_tournaments_with_status():
    """Gets tournament information by status_id."""
    query = '''
        SELECT t.id, t.tournament_name, t.start_time, t.end_time, t.status_id, u.player_name, u.discord_snowflake
        FROM tournaments t
        LEFT JOIN users u
        ON u.id = t.designer_id;
    '''
    response = db_read(query)

    return response

def get_tournament_statuses():
    """Gets list of tournament statuses."""
    query = "SELECT * FROM tournament_status_lookup;"
    response = db_read(query)

    return response

def get_tournament_user_games(u):
    """Gets list of tournaments a user is registered in."""
    query = "SELECT * FROM tournament_status WHERE user_id=%s"
    variables = (u,)
    response = db_read(query, variables)

    return response


def get_tournament_user_info(t):
    """Gets user information for users entered into a tournament."""
    query = '''
        SELECT u.*
        FROM tournament_status ts
        LEFT JOIN users u ON ts.user_id=u.id
        WHERE tournament_id=%s;
    '''
    variables = (t,)
    response = db_read(query, variables)

    return response
###############################################################################

##### Update ##################################################################
def change_tournament_status(t, c):
    """Sets tournament `t` to status `c`"""
    query = "UPDATE tournaments SET status_id=%s WHERE id=%s;"
    variables = (c, t)
    response = db_update(query, variables)

    return response

def start_user_round(t, u, r):
    """Sets user `u` to start round `r` on tournament `t`"""
    query = '''
        UPDATE tournament_status
        SET round=%s, hole=1, shot=1, location_id=1
        WHERE tournament_id=%s AND user_id=%s;
    '''
    variables = (r, t, u)
    response = db_update(query, variables)

    return response
###############################################################################

##### DELETE ##################################################################
def remove_user_from_tournament(t, u):
    """Removes user from being registered in tournament."""
    query = '''
        DELETE FROM tournament_status
        WHERE
            tournament_id=%s AND
            user_id=%s;
    '''
    variables = (t, u)
    response = db_delete(query, variables)

    return response
###############################################################################
###############################################################################

##### COURSES QUERIES #########################################################
##### Read ####################################################################
def get_all_courses():
    """Gets list of all courses."""
    query = "SELECT c.id, c.course_name, u.player_name, c.par, c.yardage FROM courses c LEFT JOIN users u ON c.designer_id = u.id;"
    response = db_read(query)
    
    return response
###############################################################################
###############################################################################

##### TOURNAMENTS QUERIES #####################################################
##### Create ##################################################################
def add_user_to_tournament(userid, tid):
    """Adds user to tournament."""
    query = '''
        INSERT INTO tournament_status
        (tournament_id, user_id)
        VALUES (%s, %s);
    '''
    variables = (userid, tid)
    response = db_create(query, variables)

    return response
###############################################################################

##### Read ####################################################################
def get_all_tournaments():
    """Gets list of all tournaments."""
    query = '''
        SELECT t.id, t.tournament_name, t.start_time, t.end_time, t.status_id, sl.status_name, u.player_name, COUNT(*) AS 'rounds'
        FROM tournaments t
        LEFT JOIN users u ON t.designer_id = u.id
        LEFT JOIN tournament_rounds tr ON tr.tournament_id = t.id
        LEFT JOIN tournament_status_lookup sl on t.status_id = sl.id;
    '''
    response = db_read(query)
    
    return response

def get_tournament_info(tid):
    """Gets list of rounds for a tournament."""
    query = '''
        SELECT t.tournament_name, u.player_name, t.description, tr.round, tr.start_time, tr.end_time, c.course_name, c.par, c.yardage
        FROM tournaments t
        LEFT JOIN users u ON t.designer_id = u.id
        LEFT JOIN tournament_rounds tr ON tr.course_id = t.id
        LEFT JOIN courses c ON tr.course_id = c.id
        WHERE t.id = %s;    
    '''
    variables = (tid)
    response = db_read(query, variables)

    return response

def get_tournament_list_by_user(ctx):
    """Gets list of tournaments by user."""
    query = '''
        SELECT ts.tournament_id
        FROM tournament_status ts
        LEFT JOIN users u on ts.user_id = u.id
        WHERE u.discord_snowflake = %s;
    '''
    variables = (ctx.author.id)
    response = db_read(query, variables)

    return response

def get_tournament_organizer(tid):
    """Gets the discord id of the tournament organizer."""
    query = '''
        SELECT u.discord_snowflake
        FROM tournaments t
        LEFT JOIN users u ON t.designer_id = u.id
        WHERE t.id = %s;
    '''
    variables = (tid)
    response = db_read(query, variables)

    return response

def get_tournament_status(tid):
    """Gets the tournament status_id of the tournament."""
    query = '''
        SELECT status_id
        FROM tournaments
        WHERE id = %s;
    '''
    variables = (tid)
    response = db_read(query, variables)

    return response
###############################################################################
###############################################################################

##### USER QUERIES ############################################################
##### Create ##################################################################
def add_user_by_discord_id(ctx):
    """Adds new user to users table with their discord snowflake."""
    player_name = ctx.author.name
    snowflake = ctx.author.id

    query = "INSERT INTO users (player_name, discord_snowflake) VALUES (%s, %s);"
    variables = (player_name, snowflake)
    response = db_create(query, variables)

    return response
###############################################################################

##### Read ####################################################################
def get_user_by_discord_id(snowflake):
    """Gets user information with their discord snowflake."""
    query = "SELECT * FROM users WHERE discord_snowflake=%s;"
    variables = (snowflake)
    response = db_read(query, variables)
    
    return response
###############################################################################

##### Update ##################################################################
def change_name_by_discord_id(ctx, new_name):
    """Changes player_name in users table by their discord snowflake."""
    snowflake = ctx.author.id
    query = "UPDATE users set player_name=%s WHERE discord_snowflake=%s;"
    variables = (new_name, snowflake)
    response = db_update(query, variables)

    return response
###############################################################################

##### Delete ##################################################################
###############################################################################
###############################################################################



##### DISCORD FUNCTIONS #######################################################
class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###############################################################################

async def setup(bot):
    await bot.add_cog(Database(bot))