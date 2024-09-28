from flask import Flask, session
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_captcha2 import FlaskCaptcha
from Config import Setting
from .Logger import GetStdoutLogger

# cli
from .cli.make import MakeCommands


from .extensions import db, ServerSession, \
    ServerMigrate, ServerMail, babel, csrf
from .utils import celery_init_app, userLocalSelector

def create_app(setting: Setting) -> Flask:
    """
        Factory Function For creating FlaskApp
    """
    app = Flask(
        __name__,
        template_folder="Templates",
    )
    app.config.from_object(setting)

    # register extensions
    # cors.init_app(app=app)
    db.init_app(app=app)  # db
    csrf.init_app(app=app) # csrf token
    ServerMail.init_app(app=app)  # mail
    ServerMigrate.init_app(db=extensions.db, app=app)  # migrate
    celery = celery_init_app(app=app)  # celery
    ServerSession.init_app(app=app)  # session
    babel.init_app(  # babel
        app=app,
        locale_selector=userLocalSelector,
        default_translation_directories=str((Setting.BASE_DIR / "translations").absolute())
    )


    # captcha config
    ServerCaptchaMaster = FlaskCaptcha(app=app)
    ServerCaptcha2 = ServerCaptchaMaster.getGoogleCaptcha2(name='g-captcha2', conf=Setting.GOOGLE_CAPTCHA_V2_CONF)
    ServerCaptcha3 = ServerCaptchaMaster.getGoogleCaptcha3(name='g-captcha3', conf=Setting.GOOGLE_CAPTCHA_V3_CONF)
    app.extensions['master-captcha'] = ServerCaptchaMaster
    app.extensions['captcha2'] = ServerCaptcha2
    app.extensions['captcha3'] = ServerCaptcha3


    # Register apps:
    from .middlewares import blp
    app.register_blueprint(blp, url_prefix='/')

    from Web import web
    app.register_blueprint(web, url_prefix="/")

    from Order import order
    app.register_blueprint(order, url_prefix="/order/")

    from Auth import auth
    app.register_blueprint(auth, url_prefix="/auth/")

    from Admin import admin
    app.register_blueprint(admin, url_prefix="/admin/")

    from User import user
    app.register_blueprint(user, url_prefix="/user/")

    from Blog import blog
    app.register_blueprint(blog, url_prefix="/blog/")

    app.SimpleLogger = GetStdoutLogger("SimpleLogger")

    # read templates and contexts
    from .template_filter import contexts, templatesFilters
    app.context_processor(contexts)

    for each in templatesFilters:
        app.add_template_filter(templatesFilters[each], name=each)

    app.wsgi_app = ProxyFix( # tell flask in behind a reverse proxy
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    return app




app = create_app(Setting())


# bind error pages to app
from . import errors
from . import tasks