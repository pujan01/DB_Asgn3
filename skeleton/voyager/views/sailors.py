from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import redirect

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

    @bp.route("/sailors/who-sailed-on-date")
    def _get_sailors_from_date():
        with get_db() as conn:
            date = request.args.get("date")
            rows = get_sailors_from_date(conn, date)
        return render_template("table.html", name="Sailors who sailed on " + date, rows=rows)

    @bp.route("/sailors/who-sailed-on-boat-of-color")
    def _get_sailors_from_boat_color():
        with get_db() as conn:
            boat_color = request.args.get("color")
            rows = get_sailors_from_boat_color(conn, boat_color)
        return render_template("table.html", name="Sailors who sailed on " + boat_color + " boats", rows=rows)
    
    @bp.route("/sailors/add")
    def _load_sailor_page():
        return render_template("addsailor.html")
    
    @bp.route("/sailors/add/post", methods = ["Post"])
    def _add_a_sailor():
        with get_db() as conn:
            sname = request.form["sname"]
            age = request.form["age"]
            exp = request.form["exp"]
            add_a_sailor(conn, sname, age, exp)
            rows = sailors(conn)
        return render_template("table.html", name="Sailors", rows=rows)

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def get_sailors_from_boat_name(conn, boat_name):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience, b.name, v.date_of_voyage FROM Sailors s , Voyages v, Boats b WHERE  b.name = :b_name AND s.sid = v.sid AND v.bid = b.bid", {'b_name': boat_name })

def get_sailors_from_date(conn, date):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience, b.name FROM Sailors s , Voyages v, Boats b WHERE  v.date_of_voyage = :v_date AND s.sid = v.sid AND v.bid = b.bid", {'v_date': date })

def get_sailors_from_boat_color(conn, boat_color):
   return execute(conn, "SELECT s.sid, s.name, s.age, s.experience, b.name, v.date_of_voyage FROM Sailors s , Voyages v, Boats b WHERE  b.color = :b_color AND s.sid = v.sid AND v.bid = b.bid", {'b_color': boat_color })




def add_a_sailor(conn, name, age, exp):
    return execute(conn, "INSERT INTO Sailors(name,age,experience) VALUES (:name,:age,:experience) ", {'name': name, 'age': age, 'experience': exp } )