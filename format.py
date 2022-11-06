import copy

CLAUSE_ORDER = [
    "_raw", "_nest", "_with", "_with_recursive", "_intersect", "_union", "_union_all", "_except", "_except_all",
    "_table",
    "select", "_select_distinct", "_select_distinct_on", "_select_top", "_select_distinct_top",
    "_into", "_bulk_collect_into",
    "_insert_into", "_update", "_delete", "_delete_from", "_truncate",
    "_columns", "_set", "from", "_using",
    "_join_by",
    "_join", "_left_join", "_right_join", "_inner_join", "_outer_join", "_full_join",
    "_cross_join",
    "_where", "_group_by", "_having",
    "_window", "_partition_by",
    "_order_by", "_limit", "_offset", "_fetch", "_for", "_lock", "_values",
    "_on_conflict", "_on_constraint", "_do_nothing", "_do_update_set", "_on_duplicate_key_update",
    "_returning",
    "_with_data"
    ]

#------------------------------------ Utilities ------------------------------------#

def ensure_list(x):
  return x if isinstance(x, list) else [x]

def quote(x, quotestyle="\""):
  if x == "*":
    return x
  else:
    return f"{quotestyle}{x}{quotestyle}"

class Param:
  def __init__(self, value):
    super().__init__()
    self.value = value

def param(value):
  return Param(value)

def isParam(x):
  return isinstance(x, Param)

#------------------------------------ Formatter ------------------------------------#

def format_identifiers(ids):
  ids = ensure_list(ids)
  sqls = []
  params = []
  for id_ in ids:
    if isParam(id_):
      sqls.append("?")
      params.append(id_.value)
    else:
      sqls.append(id_)
  return [", ".join(sqls), params]

def format_select(k, xs):
  xs = ensure_list(xs)
  [sql, params] = format_identifiers(xs)
  return [f"{k} {sql}", params]

def format_from(k, kws):
  if isinstance(kws, dict):
    return format(kws, nested=True)
  else:
    [sql, params] = format_identifiers(kws)
    return [f"{k} {sql}", params]

FORMATTER = {
    "select": format_select,
    "from": format_from,
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

format(
      {"select" : ["*"],
       "from" : ["table"],
       })
