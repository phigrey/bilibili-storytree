from bilibili_storytree import StoryGraph
from bilibili_storytree import ScriptNode, ScriptLink, ScriptVariable

aid = 12345678 # Your interactive video aid

def test_graph_1():
  # 建情节树：只有一个分支剧情模块
  root_video = {
    "index": 0,
    "cid": 23456780,
    "title": "start",
    "duration": 2
  }

  g = StoryGraph(aid=aid)
  n_root = ScriptNode(node_type="videoNode", isRoot=True)
  n_root.set_video(video=root_video)
  g._update_script_nodes([n_root]) # update graph["script"]["nodes"]
  g._sync_nodes() # create graph["nodes"]
  g._sync_vars()
  
  print()
  g.pretty_print()

def test_graph_2():
  # 建情节树: 建立一个非分支剧情模块，指向一个分支剧情模块 
  root_video = {
    "index": 0,
    "cid": 23456780,
    "title": "start",
    "duration": 2
  }
  
  goahead_video = {
    "index": 1,
    "cid": 23456781,
    "title": "go ahead",
    "duration": 1
  }

  g = StoryGraph(aid=aid)

  n_root = ScriptNode(node_type="videoNode", isRoot=True)
  n_root.set_video(video=root_video, branch=999) # 非分支剧情模块

  n_goahead = ScriptNode(node_type="videoNode") # 分支剧情模块
  n_goahead.set_video(video=goahead_video)

  linfo = {
    "text": "开始吧",
    "default": True
  }

  l_root_to_goahead = ScriptLink(nfrom=n_root, nto=n_goahead, link_type="flowLink", data=linfo) 

  g._update_script_nodes([n_root, n_goahead]) # update graph["script"]["nodes"]
  g._update_script_links([l_root_to_goahead]) # update graph["script"]["links"]
  g._sync_nodes() # create graph["nodes"]
  g._sync_vars()
 
  print()
  g.pretty_print()

def test_graph_3():
  # 建情节树：建立根为一个非分支剧情模块 n_root，指向一个分支剧情模块 n_goahead。
  #           这个分支剧情模块有两个分支: 一个是分支剧情模块 n_right，一个是分支跳转模块 n_left，跳转到同等级的分支剧情模块 n_right。
  root_video = {
    "index": 0,
    "cid": 23456780,
    "title": "start",
    "duration": 2
  }
  
  goahead_video = {
    "index": 1,
    "cid": 23456781,
    "title": "go ahead",
    "duration": 1
  }

  right_video = {
    "index": 2,
    "cid": 23456782,
    "title": "go right",
    "duration": 2
  }
  
  left_video = {
    "index": 3,
    "cid": 23456783,
    "title": "go left",
    "duration": 1
  }


  g = StoryGraph(aid=aid, hasGoto=True)

  n_root = ScriptNode(node_type="videoNode", isRoot=True)
  n_root.set_video(video=root_video, branch=999) # 非分支剧情模块

  n_goahead = ScriptNode(node_type="videoNode") # 分支剧情模块
  n_goahead.set_video(video=goahead_video)

  n_right = ScriptNode(node_type="videoNode")
  n_right.set_video(video=right_video) # 分支剧情模块

  n_left = ScriptNode(node_type="gotoNode") # 分支剧情模块


  linfo = {
    "text": "开始吧",
    "default": True
  }

  right_info = {
    "text": "向右",
    "default": True
  }

  left_info = {
    "text": "向左",
    "default": False 
  }


  l_root_to_goahead = ScriptLink(nfrom=n_root, nto=n_goahead, link_type="flowLink", data=linfo) 

  l_goahead_to_right = ScriptLink(nfrom=n_goahead, nto=n_right, link_type="flowLink", data=right_info) 
  l_goahead_to_left = ScriptLink(nfrom=n_goahead, nto=n_left, link_type="flowLink", data=left_info) 

  l_left_to_ref = ScriptLink(nfrom=n_left, nto=n_right, link_type="refLink")


  g._update_script_nodes([n_root, n_goahead, n_right, n_left]) # update graph["script"]["nodes"]
  g._update_script_links([l_root_to_goahead, l_goahead_to_right, l_goahead_to_left, l_left_to_ref]) # update graph["script"]["links"]

  g._sync_nodes() # create graph["nodes"]
  g._sync_vars()
 
  print()
  g.pretty_print()

