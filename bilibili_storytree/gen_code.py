import execjs
import os

def js_from_file(file_name):
  """
  读取js文件
  """
  with open(file_name, 'r', encoding='UTF-8') as file:
    result = file.read()

  return result

def gen_id():
  """
  Call decode.js to generate string of 10 characters
  """
  
  ctx = execjs.compile(js_from_file('{}/decode.js'.format(os.path.dirname(__file__))))
  return ctx.call("entry")

if __name__ == "__main__":
  print(gen_id())
