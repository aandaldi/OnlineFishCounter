class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///online-fish-counter.db'
    SECRET_KEY = 'keyDev'
    JWT_ACCESS_LIFESPAN = {'seconds': 30}
    JWT_REFRESH_LIFESPAN = {'minutes': 20}


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_online-fish-counter.db'
    SECRET_KEY = 'keyTesting'
    JWT_ACCESS_LIFESPAN = {'seconds': 30}
    JWT_REFRESH_LIFESPAN = {'minutes': 20}


class ProductionConfig(BaseConfig):
    DEBUG = False


# config_by_name = dict(
#     prod=ProductionConfig,
#     dev=DevelopmentConfig,
#     test=TestingConfig
# )


