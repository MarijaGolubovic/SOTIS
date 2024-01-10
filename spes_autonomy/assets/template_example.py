from jinja2 import Template

print("Tree name: ")
tree_name = input()
print(tree_name)

print("Action: ")
action = input()
print(action)

print("IgnoreObstacles: ")
ignore_obstacles = input()
if ignore_obstacles.strip() =="":
    ignore_obstacles = "false"
print(ignore_obstacles)

print("X: ")
x = input()
print(x)
name = action
ident = "\n\t\t   "
next_action_ident = "\n\t\t"

data = {
    "ACTION": action,
    "X": x,
    "NAME": name,
    "IGNORE_OBSTACLES": ignore_obstacles,
    "TREE_NAME": tree_name
}

begin = """<?xml version="1.0" encoding="UTF-8"?>
<root BTCPP_format="4">\n"""

end = """\t</BehaviorTree>
</root>"""

behavior_tree = """ <BehaviorTree ID=\"{{TREE_NAME}}\">"""

translate = """<{{ACTION}} name=\"{{NAME}}"{{Ident}}\
frame_id=\"base_link\"{{Ident}}\
ignore_obstacles=\"{{IGNORE_OBSTACLES}}\"{{Ident}}\
x=\"{{X}}\"{{Ident}}error=\"error\"/>"""

# Privremeno
tr1 = Template(translate)
tr= tr1.render(data, Ident=ident)
actions = [tr, tr]

template = begin + "\t" + behavior_tree
for action in actions:
    template += next_action_ident + action
template += "\n" + end

j2_template = Template(template)

file_name = tree_name+".xml"
with open(file_name, "w") as fajl:
    fajl.write(j2_template.render(data, Ident=ident))


print(j2_template.render(data, Ident=ident))
