import copy

CLAUSE_ORDER = [
    "_:raw", "_:nest", "_:with", "_:with_:recursive", "_:intersect", "_:union", "_:union_:all", "_:except", "_:except_:all",
    "_:table",
    ":select", "_:select_:distinct", "_:select_:distinct_:on", "_:select_:top", "_:select_:distinct_:top",
    "_:into", "_:bulk_:collect_:into",
    "_:insert_:into", "_:update", "_:delete", "_:delete_:from", "_:truncate",
    "_:columns", "_:set", ":from", "_:using",
    "_:join_:by",
    "_:join", "_:left_:join", "_:right_:join", "_:inner_:join", "_:outer_:join", "_:full_:join",
    "_:cross_:join",
    "_:where", "_:group_:by", "_:having",
    "_:window", "_:partition_:by",
    "_:order_:by", "_:limit", "_:offset", "_:fetch", "_:for", "_:lock", "_:values",
    "_:on_:conflict", "_:on_:constraint", "_:do_:nothing", "_:do_:update_:set", "_:on_:duplicate_:key_:update",
    "_:returning",
    "_:with_:data"
    ]

def tolist(x):
  return x if isinstance(x, list) else [x]

def is_keyword(s):
  """A keyword is as tring with prefix `:`.
  I.e: ":user" is a keyword, but "user" is not a keyword
  """
  return isinstance(s, str) and s.startswith(":")

def kw_to_str(kw):
  assert is_keyword(kw), f"not a keyword {kw}"
  return kw[1:]

dialect = "ANSI"
#formatter = Ansi()
prefix = "\""

def format_select(k, xs):
  xs = tolist(xs)
  print("XS:", xs)
  return [f"{kw_to_str(k)} {','.join(map(kw_to_str, xs))}", []]

def format_from(k, xs):
  if isinstance(xs, dict):
    return format(xs, nested=True)
  else:
    return [f"{kw_to_str(k)} {kw_to_str(xs)}", []]

FORMATTER = {
    ":select": format_select,
    ":from": format_from,
    }

def format(honey_sql_clause, nested=False):
  # let's not hurt the original map
  leftover = copy.deepcopy(honey_sql_clause)
  sqls = []
  params = []
  for clause in CLAUSE_ORDER:
    formatter = FORMATTER.get(clause, None)
    if formatter:
      [clause_sql, clause_params] = formatter(clause, leftover[clause])
      sqls.append(clause_sql)
      params.extend(clause_params)
      del leftover[clause]
  if leftover != {}:
    raise Exception(f"Failed to format these SQL clauses {leftover}")
  sql = " ".join(sqls)
  if nested:
    sql = f"({sql})"
  return [sql, params]
