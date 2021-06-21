# 实例
查看`tests/test_story_graph.py` 其中有多个例子和注释

# 背景知识 

### B 站制作交互视频的步骤：

* 1、上传分批视频
* 2、提交剧情树

### 故事树 StoryGraph

提交的剧情树结构为

```
data = {
  "graph": {
    "script": {
      "nodes": {}, # dict, 节点，包括了 videoNode, gotoNode 这两类
      "links": {}, # dict, node 之间连线，包括了 flowLink, refLink
      "hasGoto": True, # bool, 是否包含了跳转模块(B 站故事树 concept) 
      "editorVersion": "1.4.6",
      "createdTime": round(time.time()*1000), # int, 取现在时间，毫秒
      "currentThemeId": 0, # int, 默认主题样式
      "enableVariables": False, # bool, 使用到故事树的高级功能为 True
      "variables": [] # list[dict], 初始化时有值，但是如果剧情树没有用到高级功能，就没啥用
    }, # 描述如何绘制剧情树
    "nodes": {}, # 最终节点
    "aid": "", # int, 视频 aid
    "skin_id": 0, # int, 没什么特别需求，就默认样式
    "regional_vars": [], # list[dict], 使用剧情树高级功能的时候, 会有具体内容
  }
}
```
### 解释 `data["graph"]["script"]["nodes"]` 
* 参考 [B 站剧情树概念](https://www.bilibili.com/video/BV1n4411F7tm)

* `data["graph"]["script"]["nodes"]` 类型为 `dict`, `key` 是 `n-[10 characters]`, `value` 是
`dict`, 如下

```
script_node_info = {
  "id": id, # 'n-[10 characters]'
  "type": node_type, # videoNode：剧情分支模块, gotoNode：跳转分支模块
  "data": data, # 节点的内容信息, 其他的参数可以被理解为节点的结构信息
  "isRoot": isRoot, # 是否是起始节点
  "input": flowInput or [], # 哪些 flowLink 进了这个节点
  "output": flowOutput or [], # 哪些 flowLink 出这个节点
  "refInput": refInput or [], # 哪些 refLink 进了这个节点
  "refOutput": refOutput or [] # 哪些 refLink 出这个节点
}
```

* `script_node_info["data"]` 是 `dict`, 如下

```
data = {
  "type": 0, # 0：没有分支的节点， 1：有分支的节点， 999：非分支节点，直接跳转下一个。 PS, 这个设计有点不美，毕竟节点间的分支关系，更应该是结构性信息，放在内容的地方处理不是很优雅
  "aid": "",
  "cid": video["cid"],
  "name": name or video["title"], # 这个节点的名称
  "index": video["index"],
  "showTime": 0, # 目前没用到，不知道是什么
  "innerOptions": [], # 目前没用到，不知道是什么
  "dimension": {'width': 1920, 'height': 1080},
  "duration": video["duration"]*1000
}
```

其中 `video` 是从 API 获得的

* 非分支模块(`script_node_info["data"]["type"]=999`)：不能设置分支选项，直接跳转到下一个节点
  * 剧情分支模块 (`script_node_info["type"] = "videoNode"`): 需要设置视频信息
  * 跳转分支模块 (`script_node_info["type"] = "gotoNode"`): 需要设置跳转(已有的)节点信息
* 分支模块(`script_node_info["data"]["type"]=0 or 1`)：可以设置分支选项, 有分支为 1, 无分支为 0
  * 剧情分支模块 (`script_node_info["type"] = "videoNode"`): 需要设置视频信息
  * 跳转分支模块 (`script_node_info["type"] = "gotoNode"`): 需要设置跳转(已有的)节点信息


### 解释 `data["graph"]["script"]["links"]`
* `data["graph"]["script"]["links"]` 类型为 `dict`, `key` 是 `l-[10 characters]`, `value` 是
`dict`, 如下

```
scrip_link_info = {
  "id": 'l-[10 characters]', # str
  "type": link_type, # flowLink 如果from node 是videoNode, refLink 如果 from node 是gotoNode
  "data": data, # 连线的内容信息，其他的参数可以被理解为是连线的结构信息
  "from": nfrom_id, # 连线的开始节点 id
  "to": nto_id # 连线的结束节点 id
}
```

* `script_link_info["data"]` 是 `dict`，如下

```
data = {
  "id": link_id, # str, "l-[10 characters]"
  "point": {'x': 0, 'y': 0, 'align': 2} # Never used that, just set as default
  "conditions": [], # 在高级功能的时候会用到，其他时候都是 []
  "actions": [], # 在高级功能的时候会用到，其他时候都是 []
  "text": "我要去下个节点",
  "default": False # 从一个节点出来的连线，其中有一个是默认分支，设置为True, 其他的为 False 
}
```

### 解释 `data["graph"]["nodes"]`

* `data["graph"]["nodes"]` 是 list[dict], 只会有类型为videoNode 的信息

* 每个节点的信息如下：
```
self.info = {
  "id": "n-[10 characters]", # str
  "cid": script_node_info["data"]["cid"],
  "name": script_node_info["data"]["name"],
  "is_start": 1 if script_node_info["isRoot"] else 0, 
  "show_time": 0 if script_node_info["data"]["type"] == 999 else -1 # int, Strange semantic，no idea why
  "otype": 1, # int, No idea 
  "edges": [], # list[dict], 从这个节点出去的连线
}
``` 

### 解释高级功能

* 简而言之，就是会使用到隐藏数值来左右情节树走向的功能。用户的交互改变隐藏数值，隐藏数值改变呈现的故事情节。

* 参考 [B 站情节树高级功能](https://www.bilibili.com/video/BV134411F7VD)

重要的几个参数
* `data["graph"]["script"]["enableVariables"]` 设置为 True 如果用到高级功能
* `data["graph"]["script"]["variables"]` 默认为
```
graph_script['variables'] = [
  {'id': 'v-LMw8OzBpw', 'type': 1, 'name': '数值1', 'initValue': 0, 'initValue2': 0, 'displayable': False},
  {'id': 'v-2xvB5bPFCl', 'type': 1, 'name': '数值2', 'initValue': 0, 'initValue2': 0, 'displayable': False},
  {'id': 'v-Lh0XaHD6ND', 'type': 1, 'name': '数值3', 'initValue': 0, 'initValue2': 0, 'displayable': False},
  {'id': 'v-as5TbzlglR', 'type': 1, 'name': '数值4', 'initValue': 0, 'initValue2': 0, 'displayable': False},
  {'id': 'v-Lwe1HHANpM', 'type': 2, 'name': '随机值', 'initValue': 1, 'initValue2': 100, 'displayable': False}]
```
显而易见，其中
  * `id` 是 `v-[10 characters]`
  * `type` int, 可设置固定初始值的为 1， 随机产生的为 2
  * `name` str, 可以自己设置, 就是变量名
  * `initValue`: int, 在 type 为1的时候，初始值；在 type 为2时，就是随机数的取值下限
  * `initValue2`: int, 在 type 为1的时候，没用到；在 type 为2时，就是随机数的取值上限
  * `displayable`: bool, 是否在播放视频时显示数值
* `data["graph"]["regional_vars"]` 和 `data["graph"]["script"]["variables"]` 同步就可以, 饮用一小段代码，显而易见
```
def _sync_vars(self):
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
```

# 实现情节树的方式

* 处理 `graph["script"]` 和画图描述一致，做两个节点(`ScriptNode`)，做个连线(`ScriptLink`), 设置变量(`ScriptVariable`)
* 处理 `graph["nodes"]` 只需要同步 `graph["script"]` 就可以了, 同步接口会处理具体事情
* 处理 `graph["regional_vars"]` 只需要同步 `graph["script"]` 就可以了，同步接口会处理具体事情


