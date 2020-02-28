from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE


def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="Sailors", rows=rows)
        
    # @bp.route("/sailors/who-sailed")
    # def _get_sailors_from_boat_name():
    #     print("hewe")
    #     with get_db() as conn:
    #         boat_name = request.args.get("boat-name")
    #         print(boat_name)
    #         rows = get_sailors_from_boat_name(conn, boat_name)
    #     return render_template("table.html", name="Sailors", rows=rows)

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

# def get_sailors_from_boat_name(conn, boat_name):
#     #return execute(conn, "SELECT b.name FROM Boats b where b.name = b.name" )
#     #return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors s , Voyages v, Boats b WHERE  b.name = :boat_name", {'boat_name': bname }, s.sid = v.sid, v.bid = b.bid")

