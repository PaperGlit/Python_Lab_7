class Repository:
    def get_all(self):
        raise NotImplementedError

    def get_by_id(self, entity_id):
        raise NotImplementedError

    def add(self, data):
        raise NotImplementedError

    def update(self, entity_id, data):
        raise NotImplementedError

    def delete(self, entity_id):
        raise NotImplementedError