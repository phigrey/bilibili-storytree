from bilibili_storytree import ScriptVariable, ScriptNode, ScriptLink

def test_variable():
  # Create a variable named total, using default init value 0
  v1 = ScriptVariable(name="total", v_type=1)
  assert(v1.info["name"]=="total")
  assert(v1.info["initValue"]==0)
  assert(v1.info["initValue2"]==0)
  assert(v1.info["type"]==1)
  assert(v1.info["displayable"]==False)

  # Create a random variable named pickone, ranging from 50 to 100
  v2 = ScriptVariable(name="pickone", v_type=2, initValue=50, initValue2=80)
  assert(v2.info["name"]=="pickone")
  assert(v2.info["initValue"]==50)
  assert(v2.info["initValue2"]==80)
  assert(v2.info["type"]==2)
  assert(v2.info["displayable"]==False)

def test_videoNode():
  # Create start node with video1
  video1 = {
    "index": 0,
    "cid": 12345678,
    "title": "start",
    "duration": 2
  }
  n1 = ScriptNode(node_type="videoNode", isRoot=True)
  n1.set_video(video=video1)

  assert(n1.info["type"] == "videoNode")
  assert(n1.info["isRoot"] == True)
  assert(n1.info["data"]["cid"] == 12345678)
  assert(n1.info["data"]["name"] == "start")
  assert(n1.info["data"]["index"] == 0)
  assert(n1.info["data"]["duration"] == 2000)
  assert(n1.info["input"] == [])
  assert(n1.info["output"] == [])
  assert(n1.info["refInput"] == [])
  assert(n1.info["refOutput"] == [])

  
  # Create non-start node with video2
  video2 = {
    "index": 1,
    "cid": 23456789,
    "title": "step 1",
    "duration": 3
  }
  n2 = ScriptNode(node_type="videoNode")
  n2.set_video(video=video2, name="go ahead")

  assert(n2.info["type"] == "videoNode")
  assert(n2.info["isRoot"] == False)
  assert(n2.info["data"]["cid"] == 23456789)
  assert(n2.info["data"]["name"] == "go ahead")
  assert(n2.info["data"]["index"] == 1)
  assert(n2.info["data"]["duration"] == 3000)
  assert(n2.info["input"] == [])
  assert(n2.info["output"] == [])
  assert(n2.info["refInput"] == [])
  assert(n2.info["refOutput"] == [])


def test_flowLink():
  video1 = {
    "index": 0,
    "cid": 12345678,
    "title": "start",
    "duration": 2
  }
  n1 = ScriptNode(node_type="videoNode", isRoot=True)
  n1.set_video(video=video1)

  video2 = {
    "index": 1,
    "cid": 23456789,
    "title": "right",
    "duration": 3
  }
  n2 = ScriptNode(node_type="videoNode")
  n2.set_video(video=video2, name="go right")

  video3 = {
    "index": 1,
    "cid": 34567890,
    "title": "left",
    "duration": 3
  }
  n3 = ScriptNode(node_type="videoNode")
  n3.set_video(video=video3, name="go left")

  linfo_n1_to_n2 = {
    "text": "go right",
    "default": True,
  }
  sl_n1_n2 = ScriptLink(link_type="flowLink", nfrom=n1, nto=n2, data=linfo_n1_to_n2)
  assert(n1.info["output"] == [sl_n1_n2.id])
  assert(n2.info["input"] == [sl_n1_n2.id])

  linfo_n1_to_n3 = {
    "text": "go left",
    "default": True,
  }
  sl_n1_n3 = ScriptLink(link_type="flowLink", nfrom=n1, nto=n3, data=linfo_n1_to_n3)

  assert(n1.info["output"] == [sl_n1_n2.id, sl_n1_n3.id])
  assert(n2.info["input"] == [sl_n1_n2.id])
  assert(n3.info["input"] == [sl_n1_n3.id])

def test_gotoNode():
  n = ScriptNode(node_type="gotoNode")
  assert(n.info["type"] == "gotoNode")
  assert(n.info["data"] == {})
  assert(n.info["isRoot"] == False)
  assert(n.info["input"] == [])
  assert(n.info["output"] == [])
  assert(n.info["refInput"] == [])
  assert(n.info["refOutput"] == [])


def test_refLink():
  n1 = ScriptNode(node_type="gotoNode")

  video2 = {
    "index": 1,
    "cid": 23456789,
    "title": "right",
    "duration": 3
  }
  n2 = ScriptNode(node_type="videoNode")
  n2.set_video(video=video2, name="go left")

  sl_n1_n2 = ScriptLink(link_type="refLink", nfrom=n1, nto=n2)

  assert(n1.info["refOutput"] == [sl_n1_n2.id])
  assert(n2.info["refInput"] == [sl_n1_n2.id])



