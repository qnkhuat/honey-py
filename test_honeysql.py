from format import format

def test_shallow():
  assert format({
    ":select": ":*",
    ":from"  : ":user",
    }) == ["select * from user", []]

  #assert format({
  #  ":select": "*",
  #  ":from": ":user",
  #  ":where": [":=", ":id", 1]
  #  } == [
  #    "select * from user where id = ?",
  #    [1]
  #    ])
