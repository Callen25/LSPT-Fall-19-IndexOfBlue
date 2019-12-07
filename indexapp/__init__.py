from flask import Flask
from redis import Redis
from mockredis import mock_redis_client
from indexapp.app import bp


def create_app(test_config=None):
    """
    This function creates our flask app. If we are performing unit tests,
    it sets our redis client to be a mock redis client. It also registers
    endpoints that we are using.
    @param test_config: Tells us if we are testing or not
    @return: this app, for testing purposes or running normally
    """
    main_app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # k, v store for term -> doc_id
        main_app.index = Redis(host='localhost', port=6379, db=0)
        # k, v store for doc:term -> list of positions
        main_app.term_positions = Redis(host='localhost', port=6379, db=1)
    else:
        # Same db's as above, but the mock_redis version
        main_app.index = mock_redis_client(host='localhost', port=6379, db=0)
        main_app.term_positions = mock_redis_client(host='localhost', port=6379, db=1)
        # sets the initial value total docs for tf-idf
        main_app.index.set("total_docs", 0)
        # Specify that we are in testing config for debugging
        main_app.config['TESTING'] = True
        

    # Tells this instance of flask where our endpoints are
    main_app.register_blueprint(bp)

    return main_app
