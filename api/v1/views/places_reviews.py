#!/usr/bin/python3
"""
Places view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews',
                 strict_slashes=False,
                 methods=["GET"])
def get_all_reviews(place_id):
    """Retrieves the list of all Place objects"""
    list_reviews = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in place.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<string:review_id>',
                 strict_slashes=False,
                 methods=["GET"])
def get_review(review_id):
    """Retrieves a Place object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """Delete a Place object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """Creates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = request.get_json(force=True, silent=True)
    if review is None:
        abort(400, "Not a JSON")
    review['place_id'] = place_id
    if 'user_id' not in review.keys():
        abort(400, "Missing user_id")
    elif 'text' not in review.keys():
        abort(400, "Missing text")
    else:
        user = storage.get(User, review['user_id'])
        if user is None:
            abort(404)
        new = Review(**review)
        new.place_id = place_id
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """Update a Place object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
                pass
            else:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
