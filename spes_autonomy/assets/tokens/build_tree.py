from jinja2 import Template

NEXT_ACTION_INDENTATION = "\n\t\t"
INDENTATION = "\n\t\t   "

def load_params_from_file():
    file = open('/spesbot/ros2_ws/src/spesbot/assets/action_params.txt', 'r') # path in docker container
    lines = file.readlines()
    loaded_params = []
    for line in lines:
        line = line.strip().split(",")
        loaded_params.append(line)
    return loaded_params


def render_template(template, data):
    template = Template(template)
    rendered_template = template.render(data)
    return rendered_template


def save_tree(builded_tree):
    file_name = "/spesbot/ros2_ws/src/spesbot/assets/user_tree.xml"
    with open(file_name, "w") as fajl:
        fajl.write(builded_tree)
        

def add_content_to_specific_line(file_path, line_number, content):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines.insert(line_number - 1, content)

    with open(file_path, 'w') as file:
        file.writelines(lines)
        

def remove_content_between_lines(file_path, start_line, marker):
    try:
        with open(file_path, 'r') as f:
            linije = f.readlines()

        for i in range(start_line - 1, len(linije)):
            if marker in linije[i]:
                break

        with open(file_path, 'w') as f:
            f.writelines(linije[:start_line - 1] + linije[i:])


        print(f"Sadržaj fajla od linije {start_line} do markera '{marker}' je uspešno obrisan.")
    except FileNotFoundError:
        print(f"Fajl '{file_path}' nije pronađen.")
    except Exception as e:
        print(f"Došlo je do greške: {e}")



def build_tree():
    data = {
        "ACTION_TOKEN": None,
        "INDENTATION": INDENTATION,
        "TREE_NAME_TOKEN": None,
        "NAME_TOKEN": None,
        "X_TOKEN": None,
        "Y_TOKEN": None,
        "YAW_TOKEN": None,
        "MODE_TOKEN": None,
        "IGNORE_OBSTACLES_TOKEN": None,
        "FRAME_ID_TOKEN": None,
        "LINEAR_VELOCITY_TOKEN": None,
        "ANGULAR_VELOCITY_TOKEN": None,
        "DIRECTION_TOKEN": None,
        "IMAGE_SEGMENT_TOKEN": None,
        "KP_TOKEN": None,
        "OBJECT_CLASS_TOKEN": None,
        "TOLERANCE_TOKEN": None,
        "TYPE_TOKEN": None,
        "REPEAT_TOKEN": None,
        "NUM_CYCLES": None
    }


    tree_root_begin = """<?xml version="1.0" encoding="UTF-8"?>
    <root BTCPP_format="4">\n
    """

    tree_root_end = """\t\t</Sequence>\n\t</BehaviorTree>"""

    behavior_tree = """\t<BehaviorTree ID=\"USER_TREE">\n\t\t<Sequence>"""

    translate = """<Translate name=\"{{ACTION_TOKEN}}\"{{INDENTATION}}\
    frame_id=\"base_link\"{{INDENTATION}}\
    ignore_obstacles=\"True\"{{INDENTATION}}\
    x=\"{{X_TOKEN}}\"{{INDENTATION}}error=\"error\"/>"""
    
    fallback_begin = "\n\t\t<Fallback>"
    fallback_end = "\n\t</Fallback>"
    
    repeat_begin = "\n\t\t<Repeat num_cycles=\"{{NUM_CYCLES}}\">"
    repeat_end = "\n\t\t</Repeat>"


    move = """<Move name=\"{{ACTION_TOKEN}}"{{INDENTATION}}\
    frame_id=\"base_link\"{{INDENTATION}}mode=\"1\"{{INDENTATION}}\
    ignore_obstacles=\"True\"{{INDENTATION}}\
    x=\"0\"{{INDENTATION}}y=\"0\"{{INDENTATION}}yaw=\"{{X_TOKEN}}\"\
    {{INDENTATION}}\
    error=\"error\"{{INDENTATION}}reversing=\"0\"/>"""

    actions_templates = []

    actions = load_params_from_file()
    i=0
    fallback_it = 0
    is_fallback = False
    tree = render_template(behavior_tree, data)
    for a in range(len(actions)):
        action = actions[a]
        next_action = None
        try:
            next_action = actions[a+1]
        except Exception as e: # Check next action
            print(e)
        
        if next_action is not None and len(next_action)==1:
            if(next_action[0].split(':')[0] == "REPEAT"):
                print(next_action)
                is_repeat = True
                data["NUM_CYCLES"] = next_action[0].split(':')[1]
                tree+=render_template(repeat_begin, data)
                if len(action) == 2:
                    data["ACTION_TOKEN"] = action[0]
                    value = action[1].split(':')
                    data["X_TOKEN"] = value[1]
                    if action[0] == "TRANSLATE":
                        data["X_TOKEN"] = str(float(value[1])/100)
                        actions_templates.append(translate)
                        tree += "\t"+NEXT_ACTION_INDENTATION + render_template(translate, data)
                    else:
                        actions_templates.append(move)
                        tree += NEXT_ACTION_INDENTATION + render_template(move, data)
                    tree+=repeat_end
                    fallback_it+=1
            else:
                tree+=fallback_begin
                if len(action) == 2:
                    data["ACTION_TOKEN"] = action[0]
                    value = action[1].split(':')
                    data["X_TOKEN"] = value[1]
                    if action[0] == "TRANSLATE":
                        data["X_TOKEN"] = str(float(value[1])/100)
                        actions_templates.append(translate)
                        tree += NEXT_ACTION_INDENTATION + render_template(translate, data)
                    else:
                        actions_templates.append(move)
                        tree += NEXT_ACTION_INDENTATION + render_template(move, data)
                    
                    
                fallback_it = 0
                fallback_it+=1
                is_fallback = True
        else:    
            i+=1
            if len(action) == 2:
                data["ACTION_TOKEN"] = action[0]
                value = action[1].split(':')
                data["X_TOKEN"] = value[1]
                if action[0] == "TRANSLATE":
                    data["X_TOKEN"] = str(float(value[1])/100)
                    actions_templates.append(translate)
                    tree += NEXT_ACTION_INDENTATION + render_template(translate, data)
                else:
                    actions_templates.append(move)
                    tree += NEXT_ACTION_INDENTATION + render_template(move, data)
                
                fallback_it+=1
            if is_fallback==True and fallback_it == 2:
                tree+=fallback_end
                fallback_it=0
                is_fallback = False
    print(i)


    tree += '\n' + tree_root_end + "\n"
    start_line = 4

    file_path = "/spesbot/ros2_ws/src/spesbot/spes_behavior/behaviors/test_nodes.xml"
    marker = '<!-- ############################## -->'
    remove_content_between_lines(file_path, start_line,marker)
    
    add_content_to_specific_line(file_path, start_line, tree)
    save_tree(tree)
    
    
def read_file_content():
    file_path = "/spesbot/ros2_ws/src/spesbot/assets/user_tree.xml"
    try:
        with open(file_path, 'r') as file:
            linije = file.readlines()
        return linije
    except FileNotFoundError:
        print(f"Dont find the '{file_path}'.")
        return None
    except Exception as e:
        print(f"Error in tree saving: {e}")
        return None