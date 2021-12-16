import littlesis
from littlesis import littlesis

def test_name_to_id():
    example = 'Barack Obama'
    expected = 13503
    actual = littlesis.name_to_id(example)
    assert actual == expected
    
def test_name_to_id_2():
    example = 'Obama'
    expected = 13503
    actual = littlesis.name_to_id(example)
    assert actual == expected 
    
def test_name_to_id_3():
    example = 'obama'
    expected = 13503
    actual = littlesis.name_to_id(example)
    assert actual == expected
    
def test_name_to_id_4():
    example = 'BARACK OBAMA'
    expected = 13503
    actual = littlesis.name_to_id(example)
    assert actual == expected 
