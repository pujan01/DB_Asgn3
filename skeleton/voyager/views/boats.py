
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
        return render_template("table.html", name="Boats sailed by " + sailor_name, rows=rows)

    @bp.route("/boats/by-popularity")
    def _get_boats_by_popularity():
        with get_db() as conn:
            rows = get_boats_by_popularity(conn)
        return render_template("table.html", name="Most popular boats", rows=rows)

    @bp.route("/boats/add")
    def _load_boat_page():
        return render_template("addboat.html")
    
    @bp.route("/boats/add/post", methods = ["Post"])
    def _add_a_boat():
        with get_db() as conn:
            bname = request.form["bname"]
            color = request.form["color"]
            add_a_boat(conn, bname, color)
            rows = boats(conn)
        return render_template("table.html", name="Boats", rows=rows)
    
def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def get_boats_from_sailor_name(conn, sailor_name):
    return execute(conn, "SELECT b.name, b.color, v.date_of_voyage FROM Sailors s , Voyages v, Boats b WHERE  s.name = :s_name AND s.sid = v.sid AND v.bid = b.bid", {'s_name': sailor_name })

def get_boats_by_popularity(conn):
    return execute(conn, "SELECT b.name, b.color, COUNT(b.bid) as Total FROM Sailors s , Voyages v, Boats b WHERE s.sid = v.sid AND v.bid = b.bid GROUP BY v.bid")

def add_a_boat(conn, bname, color):
    return execute(conn, "INSERT INTO Boats(name,color) VALUES (:name,:color) ", {'name': bname, 'color': color } )