from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from services.job_service import JobService

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs")
@login_required
def list_jobs():
    """List all jobs for current user"""
    jobs = JobService.get_all_jobs(current_user.id)
    return render_template("jobs/list.html", jobs=jobs)

@jobs_bp.route("/jobs/add", methods=["GET", "POST"])
@login_required
def add_job():
    """Add a new job"""
    if request.method == "POST":
        company = request.form.get("company")
        position = request.form.get("position")
        status = request.form.get("status", "Applied")
        applied_date = request.form.get("applied_date")
        follow_up_date = request.form.get("follow_up_date")
        notes = request.form.get("notes", "")
        
        JobService.add_job(current_user.id, company, position, status, applied_date, follow_up_date, notes)
        flash("Job added successfully!", "success")
        return redirect(url_for("jobs.list_jobs"))
    
    return render_template("jobs/add.html")

@jobs_bp.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    """Edit a job"""
    job = JobService.get_job(job_id, current_user.id)
    
    if not job:
        flash("Job not found!", "danger")
        return redirect(url_for("jobs.list_jobs"))
    
    if request.method == "POST":
        company = request.form.get("company")
        position = request.form.get("position")
        status = request.form.get("status")
        applied_date = request.form.get("applied_date")
        follow_up_date = request.form.get("follow_up_date")
        notes = request.form.get("notes", "")
        
        JobService.update_job(job_id, current_user.id, company, position, status, applied_date, follow_up_date, notes)
        flash("Job updated successfully!", "success")
        return redirect(url_for("jobs.list_jobs"))
    
    return render_template("jobs/edit.html", job=job)

@jobs_bp.route("/jobs/<int:job_id>/delete", methods=["POST"])
@login_required
def delete_job(job_id):
    """Delete a job"""
    job = JobService.get_job(job_id, current_user.id)
    
    if not job:
        flash("Job not found!", "danger")
        return redirect(url_for("jobs.list_jobs"))
    
    JobService.delete_job(job_id, current_user.id)
    flash("Job deleted successfully!", "success")
    return redirect(url_for("jobs.list_jobs"))

@jobs_bp.route("/jobs/<int:job_id>/status", methods=["POST"])
@login_required
def change_status(job_id):
    """Change job status"""
    status = request.json.get("status")
    job = JobService.get_job(job_id, current_user.id)
    
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    JobService.change_status(job_id, current_user.id, status)
    return jsonify({"success": True, "status": status})