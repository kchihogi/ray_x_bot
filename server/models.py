class ModelBase:
    def __init__(self):
        self.table_name = None

    def __str__(self):
        return f"ModelBase(table_name={self.table_name})"

    def columns(self, with_type=False):
        vars = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "table_name"]
        vars.sort()
        columns = ""
        for var in vars:
            if getattr(self, var).get("primary_key"):
                if with_type:
                    columns += f"{var} {getattr(self, var)['type']} PRIMARY KEY, "
                else:
                    columns += f"{var}, "
            else:
                if with_type:
                    if getattr(self, var).get("nullable"):
                        columns += f"{var} {getattr(self, var)['type']} NULL, "
                    else:
                        columns += f"{var} {getattr(self, var)['type']}, "
                else:
                    columns += f"{var}, "
        return columns[:-2]

    def members(self):
        members = []
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "table_name":
                members.append(getattr(self, attr)["value"])
        return members

    def to_dict(self):
        return {attr: getattr(self, attr)["value"] for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "table_name"}

    def to_tuple(self):
        return tuple(self.members())

    def to_json(self):
        return str(self.to_dict())

    def setter(self):
        raise NotImplementedError

class TweetModel(ModelBase):

    def __init__(self,
        created_at=None,
        id=None,
        image=None,
        last_updated=None, 
        text=None,
        times=None,
    ):
        self.table_name = "tweets"
        self.id = {"type": "INTEGER", "primary_key": True, "value": id}
        self.text = {"type": "TEXT", "value": "'{0}'".format(text) if text is not None else None}
        self.image = {"type": "BLOB", "value": image, "nullable": True}
        self.times = {"type": "INTEGER", "value": times}
        self.created_at = {"type": "TEXT", "value": "'{0}'".format(created_at) if created_at is not None else None}
        self.last_updated = {"type": "TEXT", "value": "'{0}'".format(last_updated) if last_updated is not None else None}

    def __str__(self):
        return f"TweetModel(id={self.id}, text={self.text}, image={len(self.image['value']) if self.image['value'] is not None else None}, times={self.times}, created_at={self.created_at}, last_updated={self.last_updated})"

    def setter(self,
        created_at=None,
        id=None,
        image=None,
        last_updated=None,
        text=None,
        times=None,
    ):
        if id is not None:
            self.id = {"type": self.id["type"], "primary_key": self.id["primary_key"], "value": id}
        if text is not None:
            self.text = {"type": self.text["type"], "value": "'{0}'".format(text) if text is not None else None}
        if image is not None:
            self.image = {"type": self.image["type"], "value": image}
        if times is not None:
            self.times = {"type": self.times["type"], "value": times}
        if created_at is not None:
            self.created_at = {"type": self.created_at["type"], "value": "'{0}'".format(created_at) if created_at is not None else None}
        if last_updated is not None:
            self.last_updated = {"type": self.last_updated["type"], "value": "'{0}'".format(last_updated) if last_updated is not None else None}

if __name__ == "__main__":
    model = TweetModel()
    print("columns with type:", model.columns(with_type=True))
    print("columns:", model.columns())
    print("members:", model.members())
    print("to_dict:", model.to_dict())
    print("to_tuple:", model.to_tuple())
    print("to_json:", model.to_json())

    file_path = __file__

    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")

    if binary_data:
        print("len(binary_data):", len(binary_data))

    model.setter(1, "Hello, world!", binary_data, 1, "2021-01-01 00:00:00", "2021-01-01 00:00:01")
    print("setter:", model)
    print("to_dict:", model.to_dict())
    print("to_tuple:", model.to_tuple())
    print("to_json:", model.to_json())
