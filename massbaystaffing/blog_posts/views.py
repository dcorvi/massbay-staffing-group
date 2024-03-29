# massbaystaffing/blog_posts/views.py
from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from massbaystaffing import db
from massbaystaffing.models import BlogPost
from massbaystaffing.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts',__name__, template_folder='templates/blog_posts')

# BLOG POST - C R U D

# BLOG POST (CREATE)
@blog_posts.route('/create_blog',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created", "success")
        return redirect(url_for('core.blog'))

    elif not form.validate_on_submit() and request.method != 'GET':
        flash("Fix fields", "warning")

    return render_template('create_post.html',form=form, button='Add Blog Post', title="Create Post")


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
# BLOG POST (VIEW/READ)
@blog_posts.route('/blog-<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)

# BLOG POST (UPDATE)
@blog_posts.route("/blog-<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated', "info")
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.

    elif not form.validate_on_submit() and request.method != 'GET':
        flash("Fix fields", "warning")

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', button='Update Blog', title='Update', form=form)

# BLOG POST (DELETE)
@blog_posts.route("/blog-<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted', "info")
    return redirect(url_for('core.blog'))

# BLOG POST (DELETE)
@blog_posts.route("/blog-<int:blog_post_id>/delete1", methods=['POST'])
@login_required
def delete_post1(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post deleted', "info")
    return redirect(url_for('core.blog'))

# JOB POST (DELETE)
@blog_posts.route("/blog-<int:blog_post_id>/delete2", methods=['POST'])
@login_required
def delete_post2(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post deleted', "info")
    return redirect(url_for('users.account'))
