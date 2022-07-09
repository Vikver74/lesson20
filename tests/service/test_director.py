import pytest
from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService
from unittest.mock import MagicMock



@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)
    director1 = Director(id=1, name='Рязанов Эльдар')
    director2 = Director(id=2, name='Гайдай Леонид')
    director3 = Director(id=3, name='Масленников Игорь')
    director4 = Director(id=4, name='Данелия Георгий')
    director5 = Director(id=5, name='Меньшов Владимир')

    # director6 = Director(id='6', name='Бондарчук Сергей')

    director_dao.get_one = MagicMock(return_value=director3)
    director_dao.get_all = MagicMock(return_value=[director1,
                                                   director2,
                                                   director3,
                                                   director4,
                                                   director5,
                                                   ])
    director_dao.create = MagicMock(return_value=Director(id=6))
    director_dao.update = MagicMock(return_value=Director(name='Роу Александр'))
    director_dao.delete = MagicMock()


    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(2)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0
        assert len(directors) == 5

    def test_create(self):
        director_d = {
            "name": "Меньшов Владимир"
        }
        director = self.director_service.create(director_d)
        assert director.id is not None
        assert director.id == 6

    def test_update(self):
        director_d = {
            "id": 4,
            "name": "Роу Александр"
        }
        director = self.director_service.update(director_d)
        assert director.id is None

    def test_partially_update(self):
        director_d = {
            "id": 4,
            "name": "Роу Александр"
        }
        self.director_service.partially_update(director_d)

    def test_delete(self):
        self.director_service.delete(2)