import pytest
from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService
from unittest.mock import MagicMock


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)
    genre1 = Genre(id=1, name='комедия')
    genre2 = Genre(id=2, name='драма')
    genre3 = Genre(id=3, name='исторический')
    genre4 = Genre(id=4, name='триллер')
    genre5 = Genre(id=5, name='сказка')

    genre_dao.get_one = MagicMock(return_value=genre3)
    genre_dao.get_all = MagicMock(return_value=[genre1,
                                                   genre2,
                                                   genre3,
                                                   genre4,
                                                   genre5,
                                                   ])
    genre_dao.create = MagicMock(return_value=Genre(id=6))
    genre_dao.update = MagicMock(return_value=Genre(name='Анимэ'))
    genre_dao.delete = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(2)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0
        assert len(genres) == 5

    def test_create(self):
        genre_d = {
            "name": "мультфильм"
        }
        genre = self.genre_service.create(genre_d)
        assert genre.id is not None
        assert genre.id == 6

    def test_update(self):
        genre_d = {
            "id": 4,
            "name": "Анимэ"
        }
        genre = self.genre_service.update(genre_d)
        assert genre.name == 'Анимэ'

    def test_partially_update(self):
        genre_d = {
            "id": 4,
            "name": "Анимэ"
        }
        self.genre_service.partially_update(genre_d)

    def test_delete(self):
        self.genre_service.delete(2)