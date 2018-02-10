# _*_ coding: utf-8 _*_
# filename: view.py

from flask import render_template, redirect, request, url_for, flash, abort, current_app, make_response
from flask_login import login_required, current_user
from . import _main
from app import db
from app.models.User import User
from app.models.Post import Post
from app.models.Comment import Comment
from app.models.Role import Permission
from .form import PostForm, CommentForm
from app.decorators import permission_required


@_main.route('/')
def index():
    return redirect(url_for('main.post_blog'))


@_main.route('/postBlog', methods=['GET', 'POST'])
@login_required
def post_blog():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post_blog'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)


@_main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.post_blog')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@_main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('main.post_blog')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@_main.route('/user/<username>')
def user(username):
    uu = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=uu, posts=posts)


@_main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论成功！')
        return redirect(url_for('main.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count()-1)/current_app.config['FLASKY_COMMENTS_PER_PAGE']+1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    return render_template('main/post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@_main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('该博客已更新！')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('main/edit_post.html', form=form)


@_main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在该用户！')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash('您已经关注了该用户！')
        return redirect(url_for('user.user_center', username=username))
    current_user.follow(user)
    flash('关注了%s！'%username)
    return redirect(url_for('user.user_center', username=username))


@_main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('不存在该用户！')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash('您未关注该用户！')
        return redirect(url_for('user.user_center', username=username))
    current_user.unfollow(user)
    flash('已取消关注%s！'%username)
    return redirect(url_for('user.user_center', username=username))


@_main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('该用户不存在！')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user': item.followers, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('main/followers.html', user=user, title='Followers of',
                           endpoint='main.followers', pagination=pagination, follows=follows)


@_main.route('/followed-by')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在！')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWED_PER_PAGE'],
        error_out=False
    )
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('main/followed_by.html', user=user, title='Followed by',
                           endpoint='main.followed_by', pagination=pagination, follows=follows)


@_main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('main/moderate.html', comments=comments, pagination=pagination, page=page)


@_main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('main.moderate', page=request.args.get('page', 1, type=int)))


@_main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('main.moderate', page=request.args.get('page', 1, type=int)))