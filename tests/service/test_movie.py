import pytest
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService
from unittest.mock import MagicMock



@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)
    movie1 = Movie(id=1, title='Кавказская пленница', description='семейная комедия', trailer='http://movie1.loc', year='1970', rating=7.2, genre_id=1, director_id=5)
    movie2 = Movie(id=2, title='Бриллиантовая рука', description='золотая коллекция', trailer='http://movie2.loc', year='1960', rating=8.1, genre_id=2, director_id=4)
    movie3 = Movie(id=3, title='Александр Невский', description='исторический фильм', trailer='http://movie3.loc', year='1980', rating=7.8, genre_id=3, director_id=3)
    movie4 = Movie(id=4, title='Ирония судьбы', description='с новым годом!', trailer='http://movie4.loc', year='1990', rating=8.4, genre_id=4, director_id=2)
    movie5 = Movie(id=5, title='Кин-дза-дза', description='антиутопия', trailer='http://movie5.loc', year='1984', rating=7.6, genre_id=5, director_id=1)

    # director6 = Director(id='6', name='Бондарчук Сергей')

    movie_dao.get_one = MagicMock(return_value=movie3)
    movie_dao.get_all = MagicMock(return_value=[movie1,
                                                   movie2,
                                                   movie3,
                                                   movie4,
                                                   movie5,
                                                   ])
    movie_dao.create = MagicMock(return_value=Movie(id=6))

    movie_dao.update = MagicMock(return_value=Movie(id=4, title='Земля санникова'))

    movie_dao.delete = MagicMock()


    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(2)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0
        assert len(movies) == 5

    def test_create(self):
        movie_d = {
            "tite": "Белое солнце пустыни",
            "description": "Советский вестерн",
            "trailer": "http://movie6.loc",
            "year": "1979",
            "rating": "8.2",
            "genre_id": "4",
            "director_id": "4"
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None
        assert movie.id == 6

    def test_update(self):
        movie_d = {
            "id": 4,
            "title": "Белое солнце пустыни",
            "description": "ЛУчший советский вестерн",
            "trailer": "http://movie6.loc",
            "year": "1979",
            "rating": "8.2",
            "genre_id": "4",
            "director_id": "4"
        }
        movie = self.movie_service.update(movie_d)
        assert movie.id == 4

    def test_partially_update(self):
        movie_d = {
            "id": 4,
            "title": "Белое солнце пустыни",
            "description": "Лучший советский вестерн",
            "trailer": "http://movie6.loc"
        }
        self.movie_service.partially_update(movie_d)

    def test_delete(self):
        self.movie_service.delete(2)
