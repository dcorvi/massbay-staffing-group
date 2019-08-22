# massbaystaffing/job_posts/views.py
from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from massbaystaffing import db
from massbaystaffing.models import Job
from massbaystaffing.job_posts.forms import JobForm

job_posts = Blueprint('job_posts',__name__, template_folder='templates/job_posts')

# JOB POST - C R U D

# JOB POST (CREATE)
@job_posts.route('/create_job',methods=['GET','POST'])
@login_required
def create_job():
    form = JobForm()

    if form.validate_on_submit():

        job_post = Job(job_title=form.job_title.data, company=form.company.data, city=form.city.data, state=form.state.data, zip=form.zip.data, job_description=form.job_description.data, job_requirements=form.job_requirements.data, job_status=form.job_status.data, job_sector=form.job_sector.data, post_website=form.post_website.data, job_posting_link=form.job_posting_link.data, user_id=current_user.id)

        db.session.add(job_post)
        db.session.commit()
        flash("Job post created", "success")
        return redirect(url_for('core.positions'))

    elif not form.validate_on_submit() and request.method != 'GET':
        flash("Fix fields", "warning")

    return render_template('create_job.html',form=form, button='Add Job', title="Create Job")


# int: makes sure that the job_post_id gets passed as in integer
# instead of a string so we can look it up later.
# BLOG POST (VIEW/READ)
@job_posts.route('/job-<int:job_post_id>')
def job_post(job_post_id):
    # grab the requested job post by id number or return 404
    job_post = Job.query.get_or_404(job_post_id)
    return render_template('job_post.html',title='Job Post',post=job_post
    )

# BLOG POST (UPDATE)
@job_posts.route("/job-<int:job_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(job_post_id):
    job_post = Job.query.get_or_404(job_post_id)
    if job_post.jobposter != current_user:
        # Forbidden, No Access
        abort(403)

    form = JobForm()
    if form.validate_on_submit():
        job_post.job_title = form.job_title.data
        job_post.company = form.company.data
        job_post.city = form.city.data
        job_post.state = form.state.data
        job_post.zip = form.zip.data
        job_post.job_description = form.job_description.data
        job_post.job_requirements = form.job_requirements.data
        job_post.job_status = form.job_status.data
        job_post.job_sector = form.job_sector.data
        job_post.post_website = form.post_website.data
        job_post.job_posting_link = form.job_posting_link.data
        db.session.commit()
        flash('Job updated', "info")
        return redirect(url_for('job_posts.job_post', job_post_id=job_post.id, title='Job Post'))
    # Pass back the old job post information so they can start again with
    # the old job information.
    elif not form.validate_on_submit() and request.method != 'GET':
        flash("Fix fields", "warning")

    elif request.method == 'GET':
        form.job_title.data = job_post.job_title
        form.company.data = job_post.company
        form.city.data = job_post.city
        form.state.data = job_post.state
        form.zip.data = job_post.zip
        form.job_description.data = job_post.job_description
        form.job_requirements.data = job_post.job_requirements
        form.job_status.data= job_post.job_status
        form.job_sector.data= job_post.job_sector
        form.post_website.data= job_post.post_website
        form.job_posting_link.data = job_post.job_posting_link
    return render_template('create_job.html', button='Update Job', title='Update Job', form=form)

# BLOG POST (DELETE)
@job_posts.route("/job-<int:job_post_id>/delete1", methods=['POST'])
@login_required
def delete_post1(job_post_id):
    job_post = Job.query.get_or_404(job_post_id)
    if job_post.jobposter != current_user:
        abort(403)
    db.session.delete(job_post)
    db.session.commit()
    flash('Job post deleted', "info")
    return redirect(url_for('core.positions'))

# JOB POST (DELETE)
@job_posts.route("/job-<int:job_post_id>/delete2", methods=['POST'])
@login_required
def delete_post2(job_post_id):
    job_post = Job.query.get_or_404(job_post_id)
    if job_post.jobposter != current_user:
        abort(403)
    db.session.delete(job_post)
    db.session.commit()
    flash('Job post deleted', "info")
    return redirect(url_for('users.account'))
