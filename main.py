from json import JSONEncoder
from flask import Flask, jsonify, request

from model.post import Post


posts = []
app = Flask(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return obj.__dict__
        return super().default(obj)


app.json_encoder = CustomJSONEncoder


def generate_unique_id():

    return len(posts) + 1

@app.route('/post', methods=['POST'])
def create_post():
    post_json = request.get_json()
    new_id = generate_unique_id()
    post = Post(new_id, post_json['body'], post_json['user'])
    posts.append(post)
    return jsonify({'status': 'success', 'id': new_id})


@app.route('/post/<int:id>', methods=['PATCH'])
def update_post(id):
    for post in posts:
        if post.id == id:
            post_json = request.get_json()
            post.body = post_json['body']
            post.user = post_json['user']
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error 404'})



@app.route('/post', methods=['GET'])
def read_posts():
    return jsonify({'posts': [post.__dict__ for post in posts]})



@app.route('/post/', methods=['DELETE'])
def remove_posts():

    if len(posts) == 0:
        return ({'status': 'not found'})
    posts.remove(posts[0])
    return ({'status': 'delete'})


if __name__ == '__main__':
    app.run(debug=True)
