from app import app
from flask import render_template, send_from_directory, flash, redirect, url_for

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        total_files=1200,
        last_scan="2026-03-12 02:00",
        next_scan="2026-03-19 02:00",
        job_count=3,
        interval_hours=168
    )
