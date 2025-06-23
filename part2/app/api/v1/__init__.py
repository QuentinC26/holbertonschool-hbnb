from .reviews import api as review_ns
api.add_namespace(review_ns, path='/api/v1/reviews')
