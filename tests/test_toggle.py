from project.server import app


def test_toggle_noarg():
    """
    GIVEN a discovery with no arguments
    WHEN a discovery is run
    THEN check for a valid return code
    """
    t = app.test_client().get('/toggle')
    assert t.status_code == 404


def test_discover_invalidarg():
    """
    GIVEN a discovery with a bad argument
    WHEN a discovery is run
    THEN check for a 405
    """
    t = app.test_client().get('/toggle/asdf')
    assert t.status_code == 404


def test_discover_validarg():
    """
    GIVEN a discovery with a good argument
    WHEN a discovery is run
    THEN check for a
    """
    t = app.test_client().get('/toggle/127.0.0.1/asdf')
    assert t.status_code == 200
