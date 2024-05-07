from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from app.views import studentview, courseview


bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SECRET_KEY'] = 'ssisv4api'
    
    bootstrap.init_app(app)
    CSRFProtect(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    
    app.register_blueprint(studentview.students_bp)
    app.register_blueprint(courseview.courses_bp)
    
    return app