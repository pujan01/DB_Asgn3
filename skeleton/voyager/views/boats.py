
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute


def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)

    @bp.route("/boats/sailed-by")
    def _get_boats_from_sailor_name():
        with get_db() as conn:
            sailor_name = request.args.get("sailor-name")
            rows = get_boats_from_sailor_name(conn, sailor_name)
        return render_template("table.html", name="Boats", rows=rows)


def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def get_boats_from_sailor_name(conn, sailor_name):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Sailors s , Voyages v, Boats b WHERE b.name = boat_name, s.sid = v.sid, v.bid = b.bid", {'sailor_name': sailor_name })
