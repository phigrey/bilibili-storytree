import json
from .gen_code import gen_id

class ScriptVariable:
  """
  In order to generate element of graph["script"]["variables"]
  """

  def __init__(self, name: str, v_type: int=1, initValue: int=0, initValue2: int=0, displayable: bool=False):
    self.id = "v-" + gen_id()
    self.info = {
      "id": self.id,
      "name": name,
      "type": v_type, # 1 自定义 2 随机
      "initValue": initValue,
      "initValue2": initValue2,
      "displayable": displayable
    }

  def __str__(self):
    return json.dumps(self.info)

class ScriptNode:
  """
  In order to generate element of graph["script"]["nodes"]
  """

  def __init__(self, node_type: str, data: dict = {}, isRoot: bool = False, lInput: list = None, lOutput: list = None, refInput: list = None, refOutput: list = None): 
    self.id = "n-" + gen_id()
    self.info = {
      "id": self.id,
      "type": node_type,
      "data": data,
      "isRoot": isRoot,
      "input": lInput or [],
      "output": lOutput or [],
      "refInput": refInput or [],
      "refOutput": refOutput or [] 
    }

  def _set_id(self, snid):
    self.id = snid
    self.info["id"] = snid

  def _set_data(self, data: dict):
    self.info["data"] = data

  def _add_link(self, where: str, link: str):
    self.info[where].append(link)

  def __str__(self):
    return json.dumps(self.info)

  def _set_branch(self, branch: int):
    if self.info["type"] == "videoNode" and self.info["data"]["type"] != 999:
      self.info["data"]["type"] = branch

  def set_video(self, video: dict, name: str = None, branch: int = 0):
    data = {
      "type": branch, # 0：没有分支的节点， 1：有分支的节点， 999：非分支节点，直接跳转下一个
      "aid": "",
      "cid": video["cid"],
      "name": name or video["title"],
      "index": video["index"],
      "showTime": 0,
      "innerOptions": [],
      "dimension": {'width': 1920, 'height': 1080},
      "duration": video["duration"]*1000
    }
    self._set_data(data)

class ScriptLink:
  """
  In order to generate item of graph["script"]["links"]
  """ 

  def __init__(self, link_type: str, data: dict = {}, nfrom: ScriptNode = None, nto: ScriptNode = None):
    self.id = "l-" + gen_id() 
    self.nfrom = nfrom
    self.nto = nto

    self.info = {
      "id": self.id,
      "type": link_type,
      "data": data,
      "from": nfrom.id,
      "to": nto.id
    }

    if link_type == "flowLink":
      _data = self.info["data"]
      _data["point"] = {'x': 0, 'y': 0, 'align': 2}
      _data["id"] = self.id
      if "conditions" not in _data:
        _data["conditions"] = []
      if "actions" not in _data:
        _data["actions"] = []

    self._update_nodes()

  def _set_data(self, data: dict):
    self.info["data"].update(data)

  def _update_nodes(self):
    o_key, i_key = "output", "input"
    if self.info["type"] == "refLink":
      o_key, i_key = "refOutput", "refInput"
    self.nfrom._add_link(o_key, self.id)
    self.nto._add_link(i_key, self.id)
    self.nfrom._set_branch(1)

  def __str__(self):
    return json.dumps(self.info)

