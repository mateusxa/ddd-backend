from repository.reposity import Repository
from tests.utils.repository_entity import TestRepository


repository = Repository()


def test_save_and_get_by_id():
    entity = TestRepository("unit_test")
    created_entity = TestRepository.from_dict(repository.save(entity))

    created_id = created_entity.id
    assert created_id

    got_entity = repository.get_by_id(created_id)

    assert got_entity
    got_entity = TestRepository.from_dict(got_entity)
    
    assert created_entity.name == got_entity.name
    assert created_entity.id
    assert got_entity.id
    assert created_entity.id.value == got_entity.id.value


def test_get_all():
    entity = TestRepository("unit_test")
    created_entity = TestRepository.from_dict(repository.save(entity))

    created_id = created_entity.id
    assert created_id

    got_entity = [
        TestRepository.from_dict(search_entity) 
        for search_entity in repository.get_all(created_entity)
    ]
    
    assert len(got_entity) >= 1


def test_update():
    created_name = "unit_test"
    entity = TestRepository.from_dict(
        repository.save(
            TestRepository(created_name)
        )
    )

    updated_name = "updated_unit_test"
    entity.name = updated_name

    updated_entity = TestRepository.from_dict(repository.update(entity))
    
    assert updated_name == updated_entity.name
    
    assert entity.id
    assert updated_entity.id
    assert entity.id.value == updated_entity.id.value
    assert entity.created == updated_entity.created


def test_save_and_delete():
    entity = TestRepository("unit_test")
    created_entity = TestRepository.from_dict(repository.save(entity))

    created_id = created_entity.id
    assert created_id

    assert not repository.delete(created_id)
    
