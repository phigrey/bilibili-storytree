import json
import time
from .graph_nodes import GraphNode
from .gen_code import gen_id

class StoryGraph:

  """
  In order to generate graph information
  """
  def __init__(self, aid: int, hasGoto: bool = False, enableVars: bool = False):
    """
    Initialize story graph by setting up basic information.

    Args:
      aid (int): aid of Bilibili video
      hasGoto (bool): whether the graph has gotoNode
      enableVars (bool): whether using the advanced feature, which is variable munipulation
    """
    self.graph = {
      "aid": aid,
      "skin_id": 0,
      "regional_vars": [],
      "nodes": [],
      "script": {}  
    }
    self.graph_script_default_variables = [{'id': 'v-'+gen_id(), 'type': 1, 'name': '数值1', 'initValue': 0, 'initValue2': 0, 'displayable': False}, {'id': 'v-'+gen_id(), 'type': 1, 'name': '数值2', 'initValue': 0, 'initValue2': 0, 'displayable': False}, {'id': 'v-'+gen_id(), 'type': 1, 'name': '数值3', 'initValue': 0, 'initValue2': 0, 'displayable': False}, {'id': 'v-'+gen_id(), 'type': 1, 'name': '数值4', 'initValue': 0, 'initValue2': 0, 'displayable': False}, {'id': 'v-'+gen_id(), 'type': 2, 'name': '随机值', 'initValue': 1, 'initValue2': 100, 'displayable': False}]

    self._init_script(hasGoto, enableVars)

  def _init_script(self, hasGoto: bool, enableVars: bool):
    """
    Initialize the graph["script"]

    Args:
      hasGoto (bool): whether the graph has gotoNode
      enableVars (bool): whether using the advanced feature, which is variable munipulation
    """
    graph_script = self.graph["script"]
    graph_script["nodes"] = {}
    graph_script["links"] = {}

    graph_script['hasGoto'] = hasGoto
    graph_script['editorVersion'] = "1.4.6"
    graph_script['createdTime'] = round(time.time()*1000)
    graph_script['currentThemeId'] = 0
    graph_script['enableVariables'] = enableVars
    graph_script["variables"] = []

  def _sync_nodes(self):
    """
    Synchronize the graph["nodes"] from graph["script"], call this when the graph["script"] is complete
    """
    for _, ninfo in self.graph["script"]["nodes"].items():
      if ninfo["type"] == "videoNode":
        self.graph["nodes"].append(GraphNode(ninfo, self.graph["script"]).info)

  def _sync_vars(self):
    """
    Synchronize the graph["regional_vars"] from graph["script"], call this when the graph["script"] is complete
    """
    if len(self.graph["script"]["variables"]) == 0:
      self.graph["script"]["variables"] = self.graph_script_default_variables
    for v in self.graph["script"]["variables"]:
      _v = {
        "name": v["name"],
        "type": v["type"],
        "init_min": v["initValue"],
        "init_max": v["initValue2"],
        "is_show": 1 if v["displayable"] else 0,
        "id": v["id"] 
      }
    
      self.graph["regional_vars"].append(_v)

  def _update_script_variables(self, variables: list):
    self.graph["script"]["variables"] += [v.info for v in variables]  

  def _update_script_nodes(self, nodes: list):
    _nodes = {}
    for n in nodes:
      _nodes[n.id] = n.info
    self.graph["script"]["nodes"].update(_nodes) 

  def _update_script_links(self, links: list):
    _links = {}
    for l in links:
      _links[l.id] = l.info
    self.graph["script"]["links"].update(_links)

  def _serialize(self):
    graph = {
      "aid": self.graph["aid"],
      "skin_id": self.graph["skin_id"],
      "regional_vars": self.graph["regional_vars"],
      "nodes": self.graph["nodes"],
      "script": json.dumps(self.graph["script"]) 
    }
    return graph

  def _print_script(self, key):
    print("{} GRAPH -> SCRIPT -> {} {}".format("="*15, key.upper(),"="*15))
    _data = self.graph["script"][key]
    for _id, _info in _data.items():
      print("{}:{}".format(_id, _info))
      print("")
 
  def _print_nodes(self):
    print("{} GRAPH -> NODES {}".format("="*15, "="*15))
    _data = self.graph["nodes"]
    for _info in _data:
      for k,v in _info.items():
        print("{}:{}".format(k,v))
        print("")
      print("*"*10)
    
  def _print_vars(self):
    print("{} GRAPH -> SCRIPT -> {} {}".format("="*10, "VARIABLES", "="*10))
    for v in self.graph["script"]["variables"]:
      print(v)

    print("{} GRAPH -> REGIONAL VARS {}".format("="*15, "="*15))
    for v in self.graph["regional_vars"]:
      print(v)

  def pretty_print(self):
    self._print_script("nodes")
    self._print_script("links")
    self._print_nodes()
    self._print_vars()

