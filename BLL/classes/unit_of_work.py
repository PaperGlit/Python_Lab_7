from DAL.classes.api_repository import ApiRepository


class UnitOfWork:
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url
        self.posts = ApiRepository(f"{base_api_url}/posts")
        self.comments = ApiRepository(f"{base_api_url}/comments")
        self.albums = ApiRepository(f"{base_api_url}/albums")
        self.photos = ApiRepository(f"{base_api_url}/photos")
        self.todos = ApiRepository(f"{base_api_url}/todos")
        self.users = ApiRepository(f"{base_api_url}/users")