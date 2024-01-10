# from jinja2 import Template
# import tokens

# INDENTATION = "\n\t\t   "


# def render_template(template):
#     template = Template(template)
#     rendered_template = template.render(data)
#     return rendered_template


# def load_params_from_file():
#     file = open('/spesbot/ros2_ws/src/spesbot/assets/tokens/action_params.txt', 'r')
#     lines = file.readlines()
#     loaded_params = []
#     for line in lines:
#         line = line.strip().split(",")
#         loaded_params.append(line)
#     return loaded_params


# # def find_token_value(token):
# #     loaded_params = load_params_from_file()
# #     uppercase_list = []
# #     # Convert token name to upper case
# #     for params in loaded_params:# def find_next_action():
# #     action_indexes, loaded_params = action_patterns.find_actions()
# #     for i in range(0, len(action_indexes)):
# #         row, _ = action_indexes[i]
# #         if i == len(action_indexes) - 1:
# #             next_action = len(loaded_params)
# #         else:
# #             next_action = action_indexes[i + 1][0]
# #         for j in range(row, next_action):
# #             # action_patterns.set_tokens()
# #             print(loaded_params[j][1])
# #         print(loaded_params[row][1])
# #         template_name = convert_action_name_to_template_name(loaded_params[row][1])
# #         rendered_action = action_patterns.render_template(template_name)
# #         print(rendered_action)

# #             # print(loaded_params[i][0])

# #         uppercase_list = [[str(params[0]).upper()] + params[1:] if params else params for params in loaded_params]
# #     # Find index of wanted token in input matrix
# #     indices = [(row_index, col_index) for row_index, row in enumerate(uppercase_list) for col_index, cell in
# #                enumerate(row) if cell == token]
# #     row, col = indices[0]
# #     if token == "SEQUENCE" or token == "PARALLEL":
# #         return loaded_params[row][0].strip()
# #     if indices != 1:
# #         return loaded_params[row][1].strip()

# # def find_token_value(token):
# #     loaded_params = load_params_from_file()
# #     actions = {}

# #     for action in loaded_params:
# #     # Split the entry if it contains a comma and a space
# #         if(len(action)==2):
# #             print(action[0], action[1])
# #         else:
# #             print(action[0])
# #         # if ', ' in action[0]:
# #         #     action_name, action_value = action[0].split(', ', 1)  # Use maxsplit to only split at the first occurrence
# #         #     action_name = action_name.strip()  # Remove leading/trailing whitespaces
# #         #     print(action_name)
# #         # else:
# #         #     # If no comma and space, assume the entire entry is the action name
# #         #     actions[action[0].strip()] = action[1]


# # def find_actions():
# #     loaded_params = load_params_from_file()
# #     uppercase_list = []
# #     # Convert token name to upper case
# #     token="TRANSLATE"
# #     for params in loaded_params:
# #         uppercase_list = [[str(params[0]).upper()] + params[1:] if params else params for params in loaded_params]
# #     # Find index of wanted token in input matrix
# #     indices = [(row_index, col_index) for row_index, row in enumerate(uppercase_list) for col_index, cell in
# #                enumerate(row) if cell == token]
# #     return indices, loaded_params
# #     row, col = indices[0]
# #     if indices != 1:
# #         return loaded_params[row][1].strip()


# # def set_tokens():
# #     tokens.TREE_NAME = "USER_TREE"
# #     tokens.NAME = find_token_value("NAME")
# #     tokens.ACTION = find_token_value("ACTION")
# #     tokens.X = find_token_value("X")
# #     tokens.IMAGE_SEGMENT = find_token_value("IMAGE_SEGMENT")
# #     tokens.KP = find_token_value("KP")
# #     tokens.TOLERANCE = find_token_value("TOLERANCE")



# # set_tokens()
# # find_actions()

# data = {
#     # Default
#     "ACTION": tokens.ACTION,
#     "INDENTATION": INDENTATION,
#     "TREE_NAME": tokens.TREE_NAME,
#     "NAME": tokens.NAME,

#     # Move
#     "X": tokens.X,
#     "Y": tokens.Y,
#     "YAW": tokens.YAW,
#     "MODE": tokens.MODE,
#     "IGNORE_OBSTACLES": tokens.IGNORE_OBSTACLES,
#     "FRAME_ID": tokens.FRAME_ID,
#     "LINEAR_VELOCITY": tokens.LINEAR_VELOCITY,
#     "ANGULAR_VELOCITY": tokens.ANGULAR_VELOCITY,

#     # ImageXYawRegulation
#     "DIRECTION": tokens.DIRECTION,
#     "IMAGE_SEGMENT": tokens.IMAGE_SEGMENT,
#     "KP": tokens.KP,
#     "OBJECT_CLASS": tokens.OBJECT_CLASS,
#     "TOLERANCE": tokens.TOLERANCE,
#     "TYPE": tokens.TYPE,
#     "REPEAT":tokens.REPEAT

# }

# tree_root_begin = """<?xml version="1.0" encoding="UTF-8"?>
# <root BTCPP_format="4">\n"""

# tree_root_end = """\t</BehaviorTree>
# </root>"""

# repeat_start = """\t<Repeat num_cycles=\"{{REPEAT}}\">"""
# repeat_end="""</Repeat>"""

# behavior_tree = """ <BehaviorTree ID=\"{{TREE_NAME}}\">"""

# translate = """<{{ACTION}} name=\"{{NAME}}\"{{INDENTATION}}\
# frame_id=\"{{FRAME_ID}}\"{{INDENTATION}}\
# ignore_obstacles=\"{{IGNORE_OBSTACLES}}\"{{INDENTATION}}\
# x=\"{{X}}\"{{INDENTATION}}error=\"error\"/>"""

# image_x_yaw_regulator = """<{{ACTION}} name=\"{{NAME}}"{{INDENTATION}}\
# direction=\"{{DIRECTION}}\"{{INDENTATION}}\
# image_segment=\"{{IMAGE_SEGMENT}}\"{{INDENTATION}}\
# kp=\"{{KP}}\"{{INDENTATION}}object_class=\"{{OBJECT_CLASS}}\"\
# {{INDENTATION}}tolerance=\"{{TOLERANCE}}\"{{INDENTATION}}type=\"{{TYPE}}\"/>"""

# move = """<{{ACTION}} name=\"{{NAME}}"{{INDENTATION}}\
# frame_id={{FRAME_ID}}{{INDENTATION}}mode=\"{{MODE}}\"{{INDENTATION}}\
# ignore_obstacles=\"{{IGNORE_OBSTACLES}}\"{{INDENTATION}}\
# x=\"{{X}}\"{{INDENTATION}}y=\"{{Y}}\"{{INDENTATION}}yaw=\"{{YAW}}\"\
# {{INDENTATION}}linear_velocity=\"{{LINEAR_VELOCITY}}\"{{INDENTATION}}\
# angular_velocity=\"{{ANGULAR_VELOCITY}}\"{{INDENTATION}}\
# error=\"error\"/>"""

# # render_template(translate)
# # render_template(image_x_yaw_regulator)
# # render_template(move)
