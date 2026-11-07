class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {}
        return cls._instance

    def set_setting(self, key, value):
        self.settings[key] = value

    def get_setting(self, key):
        return self.settings.get(key)


if __name__ == "__main__":
    a = Singleton()
    b = Singleton()

    b.set_setting("language", "ru")

    print("a is b:", a is b)
    print("Настройка language через b:", b.get_setting("language"))
