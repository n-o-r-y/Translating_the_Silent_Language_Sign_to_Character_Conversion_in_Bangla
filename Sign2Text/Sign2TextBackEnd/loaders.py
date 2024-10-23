from pickle import load
from rembg import new_session


class SingletonModelLoader:
    _instance = None

    def __new__(cls, file_path=''):
        if cls._instance is None:
            cls._instance = super(SingletonModelLoader, cls).__new__(cls)
            cls._instance.model = load(open(file_path, 'rb'))

            cls._instance.model.summary()

        return cls._instance

    def get_model(self):
        return self.model


class SingletonSessionLoader:
    _instance = None

    def __new__(cls, model_name=''):
        if cls._instance is None:
            cls._instance = super(SingletonSessionLoader, cls).__new__(cls)
            cls._instance.session = new_session(model_name)

        return cls._instance

    def get_session(self):
        return self.session
