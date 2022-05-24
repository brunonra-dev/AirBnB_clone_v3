#!/usr/bin/python3
"""Create a new view for Review object that
handles all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """
    Retrieves the list of all Review objects of a Place:
    GET /api/v1/places/<place_id>/reviews
    """
    list_review = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in place.reviews:
        list_review.append(review.to_dict())

    return jsonify(list_review)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_revieew(review_id):
    """Retrieves a Review object. : GET /api/v1/reviews/<review_id>"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    Creates a Review: POST /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    post = request.get_json(silent=True)
    if post is None:
        abort(400, "Not a JSON")
    post['place_id'] = place_id
    if 'user_id' not in post.keys():
        abort(400, "Missing user_id")
    elif 'text' not in post.keys():
        abort(400, "Missing text")
    else:
        user = storage.get(User, post['user_id'])
        if user is None:
            abort(404)

        instance = Review(**post)
        instance.place_id = place_id
        instance.save()
        return jsonify(instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")
    else:
        for key, value in obj.items():
            if key in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
                pass
            else:
                setattr(review, key, value)
        storage.save()
        res = review.to_dict()
        return jsonify(res), 200
