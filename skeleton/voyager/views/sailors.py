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
        
    @bp.route("/sailors/who-sailed")
    def _get_sailors_from_boat_name():
        with get_db() as conn:
            boat_name = request.args.get("boat-name")
            rows = get_sailors_from_boat_name(conn, boat_name)
        return render_template("table.html", name="Sailors who sailed on " + boat_name, rows=rows)

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def get_sailors_from_boat_name(conn, boat_name):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience, b.name, v.date_of_voyage FROM Sailors s , Voyages v, Boats b WHERE  b.name = :b_name AND s.sid = v.sid AND v.bid = b.bid", {'b_name': boat_name })

# WHERE Voyages.date_of_voyage = :v_date", {'v_date': voyage_date})
# func (conn, "Select ... FROM ... WHERE Voyages.date_of_voyage = :v_date",  {'v_date': voyage_date})