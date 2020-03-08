from backend import db


def test_create_projects(projects_json):
    db._projects = projects_json
    # check that reassign worked
    assert db._projects == projects_json

    projects = db.get_projects()
    assert isinstance(projects, list)
    assert len(projects) > 0
