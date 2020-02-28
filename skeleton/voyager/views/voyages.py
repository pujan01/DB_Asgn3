from collections import namedtuple

from flask import render_template
from flask import request

from voyager.db import get_db, execute

def voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages AS v")

def views(bp):
    @bp.route("/voyages")
    def _voyages():
        with get_db() as conn:
            rows = voyages(conn)
        return render_template("table.html", name="Voyages", rows=rows)

    @bp.route("/voyages/add")
    def _load_voyages_page():
        return render_template("addvoyage.html")
    
    @bp.route("/voyage/add/post", methods = ["Post"])
    def _add_a_voyage():
        with get_db() as conn:
            sid = request.form["sid"]
            bid = request.form["bid"]
            date_of_voyage = request.form["Date_of_voyage"]
            add_a_voyage(conn, sid, bid, date_of_voyage)
            rows = voyages(conn)
        return render_template("table.html", name="Voyages", rows=rows)

def add_a_voyage(conn, sid, bid, Date_of_voyages):
    return execute(conn, "INSERT INTO Voyages(sid, bid, date_of_voyage) VALUES (:sid,:bid,:Date_of_voyages) ", {'sid': sid, 'bid': bid, 'Date_of_voyages': Date_of_voyages } )