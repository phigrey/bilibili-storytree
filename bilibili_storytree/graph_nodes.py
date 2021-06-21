from .gen_code import gen_id 
import json
from .convertor import reform_condition, reform_attribute

class GraphNode:
  """
  Generate item in graph["nodes"].

  """
  def __init__(self, script_node_info: dict, script: dict):
    """
    Args:
      script_node_info (dict): element in graph["script"]["nodes"]
      script (dict): graph["script"]
    """
    #print(script_node_info)
    self.id = script_node_info["id"]
    self.flow_links = script_node_info["output"]
    self.ref_links = script_node_info["refOutput"]
    self.info = {
      "id": self.id,
      "cid": script_node_info["data"]["cid"],
      "name": script_node_info["data"]["name"],
      "is_start": 1 if script_node_info["isRoot"] else 0, 
      "show_time": 0 if script_node_info["data"]["type"] == 999 else -1,
      "otype": 1, # No idea 
      "edges": [] 
    }
    self._add_edges(script)

  def _add_edges(self, script: dict):
    """
    Add edges according to graph["script"]
    """
    script_links = script["links"]
    script_nodes = script["nodes"]

    for l in self.flow_links:
      link = script_links[l]
      edge = {
        "id": link["id"],
        "title": link["data"]["text"],
        "is_default": 1 if link["data"]["default"] else 0,
      } 

      edge["condition"] = reform_condition(link["data"]["conditions"])
      edge["attribute"] = reform_attribute(link["data"]["actions"])

      if script_nodes[link["to"]]["type"] == "videoNode":
        edge["to_node_id"] = link["to"]
      elif script_nodes[link["to"]]["type"] == "gotoNode":
        edge["to_node_id"] = script_links[script_nodes[link["to"]]["refOutput"][0]]["to"]

      self.info["edges"].append(edge)

  def __str__(self):
    return json.dumps(self.info)

