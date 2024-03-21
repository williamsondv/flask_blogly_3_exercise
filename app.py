"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import Post, Tag, db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/', methods=['GET', 'POST'])
def root():
    

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)


@app.route('/users', methods=['GET','POST'])
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('index.html', users=users)

@app.route('/users/<int:user_id>')
def users_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user = user)

@app.route('/users/new', methods=['GET'])
def users_new_form():
     return render_template('/user_new.html')

@app.route('/users/new', methods=['POST'])
def users_new():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        img_url = request.form['img_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash("User added successfully!")

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def user_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html',user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_post(user_id):
   
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user_id = user_id,
        tags = tags
    )

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post_edit.html', post = post, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['post_title']
    post.content = request.form['post_content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
    
    db.session.add(post)
    db.session.commit()

    return redirect("/")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def post_delete(post_id):

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')


@app.route('/tags')
def get_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/new')
def add_tag_form():
    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def handle_add_tag():
    tag = Tag(name = request.form['name'])
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
   
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag = tag)

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tag_delete(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')
