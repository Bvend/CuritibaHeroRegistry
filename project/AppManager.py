import os

from flask import Flask


class AppManager:
    
    def __init__(self, app, test_config=None):
        self.app = app
        self.configure_app(test_config)      

    def get_app(self):
        return self.app
    
    def configure_app(self, test_config):
        # create and configure the app
        self.app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(self.app.instance_path, 'project.sqlite'),
        )

        if test_config is None:
            # load the instance config, if it exists, when not testing
            self.app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            self.app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(self.app.instance_path)
        except OSError:
            pass

        from . import db
        db.init_app(self.app)

        #from project.auth import PageAuthentification
        from . import auth
        self.app.register_blueprint(auth.bp)

        from . import blog
        self.app.register_blueprint(blog.bp)
        self.app.add_url_rule('/', endpoint='index')
    
    """def add_endpoint(self):
        self.app.add_url_rule"""