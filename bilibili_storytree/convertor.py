def _flat_range(c):
  low, high, vid = c["value"], c["value2"], c["vid"]
  
  c_low = {
    "var_id": vid,
    "value": low,
    "condition": 'gt' 
  }

  c_high = {
    "var_id": vid,
    "value": high,
    "condition": 'lt'
  }
  return [c_low, c_high]
 
def _flat_eq(c):
  c_eq = {
    "var_id": c["vid"],
    "value": c["value"],
    "condition": 'eq'
  }
  return [c_eq]

condition_map = {
  "range": _flat_range,
  "eq": _flat_eq,
}
 
def reform_condition(conds: list):
  r = []
  for c in conds:
    if c["enabled"]:
       r += condition_map[c["type"]](c) 
  return r

def reform_attribute(actions: list):
  r = []
  for e in actions:
    if e["enabled"]:
      r.append({
        "var_id": e["vid"],
        "action": e["type"],
        "value": e["value"]
      })
  return r


