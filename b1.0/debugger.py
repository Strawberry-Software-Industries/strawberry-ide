import json,os

class NoIdeJSON(Exception):
    pass

values=[["last_fp","/"],["last_fpp","/"],["col_1","#000"],["col_2","#fff"]]

if not os.path.isfile("ide.json"):
    raise NoIdeJSON("There is no \"ide.json\", run main.py first.")

with open("ide.json","r") as f:
    ide=json.load(f)
    f.close()
old_ide=ide
for a in values:
    try:
        nu=ide[a[0]]
    except KeyError:
        ide[a[0]]=a[1]
    except:
        print("Bruh wasn hier los")

if old_ide!=ide:
    with open("ide.json","w") as f:
        json.dump(ide,f)
    f.close()
