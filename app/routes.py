from app import app
from flask import render_template, send_from_directory, flash, redirect, url_for, request


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        total_files=1200,
        last_scan="2026-03-12 02:00",
        next_scan="2026-03-19 02:00",
        job_count=3,
        interval_hours=168
    )

# add the job to the db with job uuid. later on, we will read this table from the scheduler and do everything what is needed
@app.route("/add_job", methods=["GET", "POST"])
def add_job():
    print("Job added!")
    return render_template("dashboard.html")

# must scan a destination folder to archive all existing items if wanted (a job must also do this scan first)
@app.route("/scan_destination_folder", methods=["GET", "POST"])
def scan_destination_folder():
    if request.method == "POST":
        destination_path = request.form.get("destination_path")
        print(destination_path)
        subfolders = request.form.get("subfolders") # "on" is true and "None" is false
        print(subfolders)
    #return redirect("/dashboard")
    return render_template("dashboard.html")

# Run a manual scan for all jobs
@app.route("/scan", methods=["POST"])
def scan():
    print("Scan method called")
    #return redirect("/dashboard")
    return render_template("dashboard.html")

# Scan a single job
@app.route("/scan/<int:job_id>", methods=["POST"])
def scan_id(job_id):
    print("Scan id method called")
    #return redirect("/dashboard")
    return render_template("dashboard.html")

@app.route("/delete_job/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    print("Scan id method called")
    #return redirect("/dashboard")
    return render_template("dashboard.html")