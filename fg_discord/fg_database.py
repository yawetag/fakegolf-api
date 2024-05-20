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
def get_courses(c):
    """Gets courses information of course_id `c`."""
    query = '''
        SELECT * FROM courses WHERE id=%s;
    '''
    variables = (c,)
    response = db_read(query, variables)

    return response

def get_holes(c, h):
    """Gets holes information of course_id `c` and hole `h`."""
    query = '''
        SELECT * FROM holes WHERE course_id=%s and hole=%s;
    '''
    variables = (c, h)
    response = db_read(query, variables)

    return response

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

def get_shot_log(s):
    """Gets last shot information of id `s`."""
    query = '''
        SELECT * FROM shot_log WHERE id=%s;
    '''
    variables = (s,)
    response = db_read(query, variables)

    return response

def get_shot_statuses():
    """Gets list of shot statuses."""
    query = "SELECT * FROM shot_status_lookup;"
    response = db_read(query)

    return response

def get_shots_with_status():
    """Gets shot information by status_id."""
    query = '''
        SELECT ts.id,
            ts.tournament_id, t.tournament_name,
            ts.user_id, u.player_name, u.discord_snowflake,
            ts.round, ts.hole, ts.shot, ts.shot_id,
            ts.location_id, l.location_name, l.modifier_name,
            ts.status_id
        FROM tournament_status ts
        LEFT JOIN tournaments t ON ts.tournament_id=t.id
        LEFT JOIN users u ON ts.user_id=u.id
        LEFT JOIN locations_lookup l on ts.location_id=l.id;
    '''
    response = db_read(query)

    return response

def get_tournament_rounds(t, r):
    """Gets tournament_rounds info by tournament_id `t` and round `r`"""
    query = '''
        SELECT * FROM tournament_rounds WHERE tournament_id=%s AND round=%s;
    '''
    variables=(t, r)
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
def add_shot_time(s):
    """Adds current time to `shot_send_time` field of `shots` on id of `s`"""
    query = "UPDATE shot_log SET shot_request_time=NOW() WHERE id=%s;"
    variables = (s,)
    response = db_update(query, variables)

    return response

def change_shot_status(s, c):
    """Sets tournament_status `s` to status `c`"""
    query = "UPDATE tournament_status SET status_id=%s WHERE id=%s;"
    variables = (c, s)
    response = db_update(query, variables)

    return response

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
        SET round=%s, hole=1, shot=1, location_id=999, status_id=50
        WHERE tournament_id=%s AND user_id=%s;
    '''
    variables = (r, t, u)
    response = db_update(query, variables)

    return response

def update_shotid_to_tournament_status(s, sid):
    """Sets shot_id `sid` to id `s`"""
    query = '''
        UPDATE tournament_status
        SET shot_id=%s
        WHERE id=%s;
    '''
    variables = (sid, s)
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

##### HOLES QUERIES ###########################################################
##### Create ##################################################################
###############################################################################

##### Read ####################################################################
def get_shot_status_by_user(u):
    """Gets shot status of user `u`"""
    query = '''SELECT * FROM tournament_status WHERE user_id=%s;'''
    variables = (u,)
    response = db_read(query, variables)

    return response
###############################################################################

##### Update ##################################################################
def insert_swing_in_shot_log(i, s):
    """Adds swing `s` to id `i`"""
    query = '''
        UPDATE shot_log
        SET user_shot = %s, shot_send_time=NOW()
        WHERE id=%s;
    '''
    variables = (s, i)
    response = db_update(query, variables)

    return response
###############################################################################

##### Delete ##################################################################
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
def add_shot_to_shot_log(tr, h, bp, s):
    """Adds new row to shot log."""
    query = '''
        INSERT INTO shot_log
        (
            tournament_id, round_id, round_num, course_id, hole_id, hole_num,
            user_id, player_name,
            shot_num, location_id, location_name, modifier_name,
            rough_penalty, deep_rough_penalty, bunker_penalty,
            oob_bonus, water_bonus, drive_bonus
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s,
            %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s
        );
    '''
    variables = (
        s['tournament_id'], tr['id'], s['round'], tr['course_id'], h['id'], s['hole'],
        s['user_id'], s['player_name'],
        s['shot'], s['location_id'], s['location_name'], s['modifier_name'],
        bp['rough'], bp['deep_rough'], bp['bunker'],
        bp['oob'], bp['water'], bp['drive']
    )
    response = db_create(query, variables)

    return response

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