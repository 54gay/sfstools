import math, json, os
from PIL import Image
from kivy.app import App
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from android.storage import primary_external_storage_path
from android.permissions import request_permissions, Permission
path_alpha = os.path.join(primary_external_storage_path(), "SFS Tools")
bp_folder_path = os.path.join(path_alpha, "Blueprints Folder")
font_folder_path = os.path.join(path_alpha, "Fonts")
image_folder_path = os.path.join(path_alpha, "Images")

# 创建目录结构
try:
    os.mkdir(path_alpha)
except FileExistsError:
    pass

try:
    os.mkdir(bp_folder_path)
except FileExistsError:
    pass

try:
    os.mkdir(font_folder_path)
except FileExistsError:
    pass

try:
    os.mkdir(image_folder_path)
except FileExistsError:
    pass


def getcolorfunc(rgb):
    """根据RGB值获取最接近的颜色名称"""
    distance = []
    colors = [
        (255, 255, 255, 'Color_White'),
        (104, 105, 104, 'Color_Gray'),
        (242, 164, 93, 'Color_Orange'),
        (64, 64, 64, 'Color_Black'),
        (70, 96, 136, 'Array'),
        (208, 131, 22, 'Gold_Foil')
    ]
    
    for item in colors:
        dist = math.sqrt((item[0] - rgb[0]) ** 2 + (item[1] - rgb[1]) ** 2 + (item[2] - rgb[2]) ** 2)
        distance.append((dist, item[3]))
    
    distance.sort()
    return distance[0][1]


class RingGeneratorScreen(Screen):
    pass


class OrientationScreen(Screen):
    pass


class PartAlignerScreen(Screen):
    pass


class FontGeneratorScreen(Screen):
    pass


class ImageConverterScreen(Screen):
    pass


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.transition = FadeTransition()


# 加载Kivy界面文件
Builder.load_file("Assets/mainkv.kv")
Builder.load_file("Assets/ring_generator.kv")
Builder.load_file("Assets/orientation.kv")
Builder.load_file("Assets/part_aligner.kv")
Builder.load_file("Assets/font_generator.kv")
Builder.load_file("Assets/image_converter.kv")


class GeneralSpinner(Spinner):
    def __init__(self, **kwargs):
        super(GeneralSpinner, self).__init__(**kwargs)
        self.paths = [bp_folder_path, font_folder_path, image_folder_path]
        self.path_index = 0

    def update_spinner(self):
        self.values = []
        if os.path.exists(self.paths[self.path_index]):
            for dirfile in os.listdir(self.paths[self.path_index]):
                self.values.append(dirfile)


class SpinnerOptions(SpinnerOption):
    def __init__(self, **kwargs):
        super(SpinnerOption, self).__init__(**kwargs)
        self.background_normal = "Assets/Button_Gray_Down.png"
        self.background_down = "Assets/Button_Gray_Up.png"
        self.height = sp(40)


class RingGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(RingGenerator, self).__init__(**kwargs)
        self.orientation = "vertical"

    def validate_slider_angle(self, widget):
        while 360 % widget.value != 0:
            widget.value += 1
        self.ids.RG_Angle_Value.text = str(widget.value) + "°"

    def change_tbutton_state(self, widget):
        # 适配中文文本
        if widget.state == "normal":
            widget.text = "否"
        else:
            widget.text = "是"

    def RG_generate_blueprint(self):
        self.ids.RG_Gen.text = "生成"
        self.ids.RG_Gen.background_normal = "Assets/Button_Red_Up.png"
        
        try:
            ring_x = float(self.ids.RG_X.text)
            ring_y = float(self.ids.RG_Y.text)
            segment_w = float(self.ids.RG_Segment_Width.text)
            segment_angle_increment = float(self.ids.RG_Angle_Value.text[:-1])  # 移除度符号
            inner_diameter = float(self.ids.RG_Inner_Diameter.text)
            inner_radius = inner_diameter / 2
            
            radius = inner_radius / math.cos(math.radians(segment_angle_increment / 2))
            segment_n = int(360 / segment_angle_increment)
            segment_h = math.sin(math.radians(segment_angle_increment / 2)) * radius * 2
            
            root_segment_x = ring_x + inner_radius - segment_w / 2
            root_segment_y = ring_y - 1.5 * segment_h
            segment_angle_1 = -segment_angle_increment
            segment_list = []
            new_name = self.ids.RG_Blueprint_Name.text
            fragment = self.ids.RG_Fragment.text
            
            for segment in range(segment_n):
                segment_angle_2 = segment_angle_1 + segment_angle_increment
                if segment == 0:
                    segment_angle_1 = 0
                
                w_b = math.sin(math.radians(segment_angle_1)) * (segment_w / 2)
                w_a = math.cos(math.radians(segment_angle_1)) * (segment_w / 2)
                h_b = math.sin(math.radians(segment_angle_1)) * segment_h
                h_a = math.cos(math.radians(segment_angle_1)) * segment_h
                
                root_x = root_segment_x - h_b + w_a
                root_y = root_segment_y + h_a + w_b
                
                w_b = math.sin(math.radians(segment_angle_2)) * (segment_w / 2)
                w_a = math.cos(math.radians(segment_angle_2)) * (segment_w / 2)
                
                part_x = root_x - w_a
                part_y = root_y - w_b
                
                segment_list.append([part_x, part_y, segment_w, segment_angle_2])
                segment_angle_1 = segment_angle_2
                root_segment_x = part_x
                root_segment_y = part_y
            
            # 创建蓝图目录
            name_addition = 0
            original_new_name = new_name
            path = os.path.join(bp_folder_path, str(new_name))
            path_2_b = os.path.join(path, "Blueprint.txt")
            path_2_v = os.path.join(path, "Version.txt")
            
            while True:
                try:
                    os.mkdir(path)
                    break
                except FileExistsError:
                    name_addition += 1
                    new_name = f"{original_new_name} {name_addition}"
                    path = os.path.join(bp_folder_path, str(new_name))
                    path_2_b = os.path.join(path, "Blueprint.txt")
                    path_2_v = os.path.join(path, "Version.txt")
            
            # 写入版本文件
            with open(path_2_v, "w+") as v:
                v.write("1.5.2.5")
            
            # 写入蓝图文件
            with open(path_2_b, "w+") as f:
                delta = {}
                delta["center"] = 9.0
                delta["offset"] = {"x": 0.0, "y": 0.0}
                delta["parts"] = []
                
                for i in segment_list:
                    # 确定纹理方向和宽度
                    if self.ids.RG_Reverse_Textures.text == "是":  # 适配中文
                        if 45.0000038 > i[3] or i[3] > 225:
                            n = -1
                            f_w = 3.4
                        else:
                            n = 1
                            f_w = 2.6
                    elif 45.0000038 <= i[3] <= 225:
                        n = -1
                        f_w = 3.4
                    else:
                        n = 1
                        f_w = 2.6
                    
                    save_part = {}
                    if self.ids.RG_Part_Type.text == "Battery":
                        save_part["n"] = "Placeholder Battery"
                    else:
                        save_part["n"] = self.ids.RG_Part_Type.text
                    
                    save_part["p"] = {"x": i[0], "y": i[1]}
                    save_part["o"] = {"x": i[2] / 3 * n, "y": segment_h, "z": i[3]}
                    save_part["t"] = "-Infinity"
                    save_part["N"] = {}
                    
                    if self.ids.RG_Part_Type.text == "Fuel Tank":
                        save_part["N"]["width_original"] = 3.0 * n
                        save_part["N"]["width_a"] = 3.0 * n
                        save_part["N"]["width_b"] = 3.0 * n
                        save_part["N"]["height"] = 1.0
                        save_part["N"]["fuel_percent"] = 1.0
                        save_part["T"] = {
                            "color_tex": self.ids.RG_Color_Tex.text,
                            "shape_tex": self.ids.RG_Shape_Tex.text
                        }
                    elif self.ids.RG_Part_Type.text == "Fairing":
                        save_part["N"]["width_original"] = f_w * n
                        save_part["N"]["width_a"] = f_w * n
                        save_part["N"]["width_b"] = f_w * n
                        save_part["N"]["height"] = 1.0
                        save_part["N"]["force_percent"] = 0.5
                        save_part["T"] = {
                            "fragment": fragment,
                            "color_tex": self.ids.RG_Color_Tex.text,
                            "shape_tex": self.ids.RG_Shape_Tex.text
                        }
                    else:
                        save_part["N"]["width"] = 3.0 * n
                        save_part["o"]["y"] *= 2
                    
                    delta["parts"].append(save_part)
                
                delta["stages"] = []
                json.dump(delta, f, indent=2)
                
        except ValueError:
            self.ids.RG_Gen.text = "检查输入"
            self.ids.RG_Gen.background_normal = "Assets/Button_Orange_Up.png"
        except Exception as e:
            self.ids.RG_Gen.text = "错误"
            self.ids.RG_Gen.background_normal = "Assets/Button_Orange_Up.png"


class Orientation(BoxLayout):
    def __init__(self, **kwargs):
        super(Orientation, self).__init__(**kwargs)
        self.orientation = "vertical"

    def orientation_type(self, widget):
        # 适配中文操作类型
        if widget.text == "X轴翻转":
            self.ids.OR_Y.disabled = True
            self.ids.OR_X.disabled = False
            self.ids.OR_Variable.disabled = True
            self.ids.OR_Scale_Fuel.disabled = True
        elif widget.text == "Y轴翻转":
            self.ids.OR_Y.disabled = False
            self.ids.OR_X.disabled = True
            self.ids.OR_Variable.disabled = True
            self.ids.OR_Scale_Fuel.disabled = True
        elif widget.text == "Z轴旋转":
            self.ids.OR_Y.disabled = False
            self.ids.OR_X.disabled = False
            self.ids.OR_Variable_Label.text = "Z角度:"
            self.ids.OR_Variable.disabled = False
            self.ids.OR_Scale_Fuel.disabled = True
        elif widget.text == "缩放":
            self.ids.OR_Y.disabled = False
            self.ids.OR_X.disabled = False
            self.ids.OR_Variable_Label.text = "缩放比例(小数):"
            self.ids.OR_Variable.disabled = False
            self.ids.OR_Scale_Fuel.disabled = False

    def change_tbutton_state(self, widget):
        # 适配中文文本
        if widget.state == "normal":
            widget.text = "否"
        else:
            widget.text = "是"

    def OR_generate_blueprint(self):
        self.ids.OR_Gen.text = "生成"
        self.ids.OR_Gen.background_normal = "Assets/Button_Red_Up.png"
        
        try:
            folder_name = self.ids.BP_S.text
            new_name = self.ids.OR_Blueprint_Name.text
            path_f = os.path.join(bp_folder_path, str(folder_name))
            path_b = os.path.join(path_f, "Blueprint.txt")
            
            with open(path_b, "r") as f:
                data = json.load(f)
            
            or_x = self.ids.OR_X.text
            or_y = self.ids.OR_Y.text
            
            # 适配中文操作类型
            if self.ids.OR_Type.text == "X轴翻转":
                for load_part in data["parts"]:
                    load_part["p"]["x"] = 2 * float(or_x) - load_part["p"]["x"]
                    load_part["o"]["x"] = -load_part["o"]["x"]
                    load_part["o"]["z"] = 360 - load_part["o"]["z"]
                    
            elif self.ids.OR_Type.text == "Y轴翻转":
                for load_part in data["parts"]:
                    load_part["p"]["y"] = 2 * float(or_y) - load_part["p"]["y"]
                    load_part["o"]["x"] = -load_part["o"]["x"]
                    load_part["o"]["z"] = 180 - load_part["o"]["z"]
                    
            elif self.ids.OR_Type.text == "Z轴旋转":
                # 计算中心点
                x_coords = [part["p"]["x"] for part in data["parts"]]
                y_coords = [part["p"]["y"] for part in data["parts"]]
                x_midpoint = sum(x_coords) / len(x_coords)
                y_midpoint = sum(y_coords) / len(y_coords)
                
                rotate_angle = float(self.ids.OR_Variable.text)
                
                for load_part in data["parts"]:
                    # 调整部件方向
                    if load_part["o"]["y"] < 0:
                        load_part["o"]["z"] += 180
                        load_part["o"]["x"] *= -1
                        load_part["o"]["y"] *= -1
                    
                    load_part["o"]["z"] += rotate_angle
                    
                    # 计算旋转后的位置
                    dx = load_part["p"]["x"] - x_midpoint
                    dy = load_part["p"]["y"] - y_midpoint
                    
                    # 计算原始角度和距离
                    distance = math.sqrt(dx**2 + dy**2)
                    original_angle = math.degrees(math.atan2(dy, dx))
                    
                    # 计算新角度
                    new_angle = original_angle + rotate_angle
                    
                    # 计算新位置
                    new_dx = distance * math.cos(math.radians(new_angle))
                    new_dy = distance * math.sin(math.radians(new_angle))
                    
                    load_part["p"]["x"] = x_midpoint + new_dx
                    load_part["p"]["y"] = y_midpoint + new_dy
                    
            elif self.ids.OR_Type.text == "缩放":
                scale_factor = float(self.ids.OR_Variable.text)
                scale_x = float(self.ids.OR_X.text)
                scale_y = float(self.ids.OR_Y.text)
                
                for load_part in data["parts"]:
                    load_part["o"]["x"] *= scale_factor
                    load_part["o"]["y"] *= scale_factor
                    load_part["p"]["x"] = scale_factor * load_part["p"]["x"] - scale_factor * scale_x + scale_x
                    load_part["p"]["y"] = scale_factor * load_part["p"]["y"] - scale_factor * scale_y + scale_y
                    
                    if self.ids.OR_Scale_Fuel.text == "是" and load_part["n"] == "Fuel Tank":  # 适配中文
                        if "fuel_percent" in load_part.get("N", {}):
                            load_part["N"]["fuel_percent"] *= scale_factor
            
            # 创建新的蓝图目录
            name_addition = 0
            original_new_name = new_name
            path = os.path.join(bp_folder_path, str(new_name))
            path_2_b = os.path.join(path, "Blueprint.txt")
            path_2_v = os.path.join(path, "Version.txt")
            
            while True:
                try:
                    os.mkdir(path)
                    break
                except FileExistsError:
                    name_addition += 1
                    new_name = f"{original_new_name} {name_addition}"
                    path = os.path.join(bp_folder_path, str(new_name))
                    path_2_b = os.path.join(path, "Blueprint.txt")
                    path_2_v = os.path.join(path, "Version.txt")
            
            # 写入文件
            with open(path_2_v, "w+") as v:
                v.write("1.5.2.5")
            
            with open(path_2_b, "w+") as f:
                json.dump(data, f, indent=2)
                
        except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError):
            self.ids.OR_Gen.text = "检查输入"
            self.ids.OR_Gen.background_normal = "Assets/Button_Orange_Up.png"
        except Exception as e:
            self.ids.OR_Gen.text = "错误"
            self.ids.OR_Gen.background_normal = "Assets/Button_Orange_Up.png"


class PartAligner(BoxLayout):
    def __init__(self, **kwargs):
        super(PartAligner, self).__init__(**kwargs)
        self.orientation = "vertical"

    def change_left_right_state(self, widget):
        # 适配中文文本
        if widget.state == "normal":
            widget.text = "左"
        else:
            widget.text = "右"

    def show_coordinates(self):
        self.ids.PA_Gen.text = "生成"
        self.ids.PA_Gen.background_normal = "Assets/Button_Red_Up.png"
        
        try:
            part_a_x = float(self.ids.AL_R_X.text)
            part_a_y = float(self.ids.AL_R_Y.text)
            part_a_z = float(self.ids.AL_R_Z.text)
            part_a_w = float(self.ids.AL_R_W.text)
            part_a_h = float(self.ids.AL_R_H.text)
            part_b_z = float(self.ids.AL_A_Z.text)
            part_b_w = float(self.ids.AL_A_W.text)
            
            # 计算部件A的边界点
            w_b = math.sin(math.radians(part_a_z)) * (part_a_w / 2)
            w_a = math.cos(math.radians(part_a_z)) * (part_a_w / 2)
            h_b = math.sin(math.radians(part_a_z)) * part_a_h
            h_a = math.cos(math.radians(part_a_z)) * part_a_h
            
            if self.ids.AL_Side.text == "左":  # 适配中文
                root_x = part_a_x - h_b - w_a
                root_y = part_a_y + h_a - w_b
                side = 1
            else:  # 右
                root_x = part_a_x - h_b + w_a
                root_y = part_a_y + h_a + w_b
                side = -1
            
            # 计算部件B的位置
            w_b = math.sin(math.radians(part_b_z)) * (part_b_w / 2)
            w_a = math.cos(math.radians(part_b_z)) * (part_b_w / 2)
            
            self.ids.AL_A_X.text = str(round(root_x + w_a * side, 3))
            self.ids.AL_A_Y.text = str(round(root_y + w_b * side, 3))
            
        except ValueError:
            self.ids.PA_Gen.text = "检查输入"
            self.ids.PA_Gen.background_normal = "Assets/Button_Orange_Up.png"


class FontGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(FontGenerator, self).__init__(**kwargs)
        self.orientation = "vertical"

    def validate_text_contents(self, widget):
        try:
            font_name = self.ids.FG_S.text
            font_path = os.path.join(font_folder_path, font_name)
            font = os.path.join(font_path, "FontInfo.txt")
            
            with open(font, "r") as f:
                font_info = json.load(f)
                allowed_symbols = font_info["letters"]
            
            copy_text = widget.text
            for letter in copy_text:
                if letter not in allowed_symbols and letter != " ":
                    widget.text = "不支持的符号!"
                    return
                    
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            pass

    def FG_generate_blueprint(self):
        self.ids.FG_Text.background_normal = "Assets/Normal_Button_Down.png"
        self.ids.FG_Gen.text = "生成"
        self.ids.FG_Gen.background_normal = "Assets/Button_Red_Up.png"
        
        try:
            font_name = self.ids.FG_S.text
            font_path = os.path.join(font_folder_path, font_name)
            font_info_path = os.path.join(font_path, "FontInfo.txt")
            
            with open(font_info_path, "r") as f:
                font_info = json.load(f)
                word_spacing = font_info["info"]["word_spacing"]
                kerning_indent_max = font_info["info"]["kerning_indent_max"]
                kerning_indent_min = font_info["info"]["kerning_indent_min"]
                allowed_symbols = font_info["letters"]
            
            center_x = float(self.ids.FG_X.text)
            center_y = float(self.ids.FG_Y.text)
            text = self.ids.FG_Text.text
            spacing_addition = float(self.ids.FG_HS.text)
            
            # 验证文本
            for letter in text:
                if letter not in allowed_symbols and letter != " ":
                    raise ValueError("不支持的符号")
            
            # 计算文本总长度
            text_length = 0
            top_right = 3
            bottom_right = 0
            letter_width = 0
            
            for letter in text:
                if letter == " ":
                    text_length += word_spacing + spacing_addition
                else:
                    letter_file = os.path.join(font_path, f"{letter}.txt")
                    with open(letter_file, "r") as f:
                        letter_data = json.load(f)
                    
                    top_left = letter_data["info"]["top_left"]
                    bottom_left = letter_data["info"]["bottom_left"]
                    
                    # 计算字间距
                    spacing_offset = kerning_indent_max
                    
                    # 根据字形特征调整间距
                    if top_left == 1 and top_right == 0:
                        spacing_offset = kerning_indent_min
                    elif top_left == 0 and top_right == 1:
                        spacing_offset = kerning_indent_min
                    
                    if bottom_left == 1 and bottom_right == 0:
                        spacing_offset = kerning_indent_min
                    elif bottom_left == 0 and bottom_right == 1:
                        spacing_offset = kerning_indent_min
                    
                    if top_left == 2 and top_right == 0:
                        spacing_offset = kerning_indent_max
                    elif top_left == 0 and top_right == 2:
                        spacing_offset = kerning_indent_max
                    
                    if bottom_left == 2 and bottom_right == 0:
                        spacing_offset = kerning_indent_max
                    elif bottom_left == 0 and bottom_right == 2:
                        spacing_offset = kerning_indent_max
                    
                    if bottom_left == 1 and bottom_right == 2:
                        spacing_offset = kerning_indent_max
                    elif bottom_left == 2 and bottom_right == 1:
                        spacing_offset = kerning_indent_max
                    
                    if top_left == 1 and top_right == 2:
                        spacing_offset = kerning_indent_max
                    elif top_left == 2 and top_right == 1:
                        spacing_offset = kerning_indent_max
                    
                    if top_left == 2 and top_right == 2:
                        spacing_offset = kerning_indent_max
                    elif top_left == 2 and top_right == 3:
                        spacing_offset = 0
                    
                    text_length += letter_width + spacing_offset + spacing_addition
                    
                    # 更新右侧特征
                    top_right = letter_data["info"]["top_right"]
                    bottom_right = letter_data["info"]["bottom_right"]
                    letter_width = letter_data["info"]["width"]
            
            # 创建蓝图
            text_x = center_x - text_length / 2
            delta = {
                "center": 9.0,
                "offset": {"x": 0.0, "y": 0.0},
                "parts": [],
                "stages": []
            }
            
            top_right = 3
            bottom_right = 0
            letter_width = 0
            
            for letter in text:
                if letter == " ":
                    text_x += word_spacing + spacing_addition
                else:
                    letter_file = os.path.join(font_path, f"{letter}.txt")
                    with open(letter_file, "r") as f:
                        letter_data = json.load(f)
                    
                    top_left = letter_data["info"]["top_left"]
                    bottom_left = letter_data["info"]["bottom_left"]
                    
                    # 计算字间距
                    spacing_offset = 0.1
                    
                    # 根据字形特征调整间距（与上面相同的逻辑）
                    if top_left == 1 and top_right == 0:
                        spacing_offset = kerning_indent_min
                    elif top_left == 0 and top_right == 1:
                        spacing_offset = kerning_indent_min
                    
                    if bottom_left == 1 and bottom_right == 0:
                        spacing_offset = kerning_indent_min
                    elif bottom_left == 0 and bottom_right == 1:
                        spacing_offset = kerning_indent_min
                    
                    if top_left == 2 and top_right == 0:
                        spacing_offset = kerning_indent_max
                    elif top_left == 0 and top_right == 2:
                        spacing_offset = kerning_indent_max
                    
                    if bottom_left == 2 and bottom_right == 0:
                        spacing_offset = kerning_indent_max
                    elif bottom_left == 0 and bottom_right == 2:
                        spacing_offset = kerning_indent_max
                    
                    if bottom_left == 1 and bottom_right == 2:
                        spacing_offset = kerning_indent_max
                    elif bottom_left == 2 and bottom_right == 1:
                        spacing_offset = kerning_indent_max
                    
                    if top_left == 1 and top_right == 2:
                        spacing_offset = kerning_indent_max
                    elif top_left == 2 and top_right == 1:
                        spacing_offset = kerning_indent_max
                    
                    if top_left == 2 and top_right == 2:
                        spacing_offset = kerning_indent_max
                    elif top_left == 2 and top_right == 3:
                        spacing_offset = 0
                    
                    text_x += letter_width + spacing_offset + spacing_addition
                    
                    # 添加部件
                    for part in letter_data["parts"]:
                        new_part = part.copy()
                        new_part["p"]["x"] += text_x
                        new_part["p"]["y"] += center_y
                        
                        if "T" in new_part:
                            new_part["T"]["color_tex"] = self.ids.FG_Color_Tex.text
                        
                        delta["parts"].append(new_part)
                    
                    # 更新右侧特征
                    top_right = letter_data["info"]["top_right"]
                    bottom_right = letter_data["info"]["bottom_right"]
                    letter_width = letter_data["info"]["width"]
            
            # 创建蓝图目录
            new_name = self.ids.FG_Blueprint_Name.text
            name_addition = 0
            original_new_name = new_name
            path = os.path.join(bp_folder_path, str(new_name))
            path_2_b = os.path.join(path, "Blueprint.txt")
            path_2_v = os.path.join(path, "Version.txt")
            
            while True:
                try:
                    os.mkdir(path)
                    break
                except FileExistsError:
                    name_addition += 1
                    new_name = f"{original_new_name} {name_addition}"
                    path = os.path.join(bp_folder_path, str(new_name))
                    path_2_b = os.path.join(path, "Blueprint.txt")
                    path_2_v = os.path.join(path, "Version.txt")
            
            # 写入文件
            with open(path_2_v, "w+") as v:
                v.write("1.5.2.5")
            
            with open(path_2_b, "w+") as f:
                json.dump(delta, f, indent=2)
                
        except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as e:
            self.ids.FG_Text.background_normal = "Assets/Button_False.png"
            self.ids.FG_Gen.text = "检查输入/不支持的符号"
            self.ids.FG_Gen.background_normal = "Assets/Button_Orange_Up.png"
        except Exception as e:
            self.ids.FG_Gen.text = "错误"
            self.ids.FG_Gen.background_normal = "Assets/Button_Orange_Up.png"


class ImageConverter(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageConverter, self).__init__(**kwargs)
        self.orientation = "vertical"

    def change_type(self, widget, value1, value2, mono):
        # value1和value2已经是界面显示的中文文本
        if widget.state == "normal":
            widget.text = str(value1)
            if mono == "mono":
                self.ids.IC_Color_Tex.disabled = False
        else:
            widget.text = str(value2)
            if mono == "mono":
                self.ids.IC_Color_Tex.disabled = True

    def IC_generate_blueprint(self):
        self.ids.IC_Gen.text = "生成"
        self.ids.IC_Gen.background_normal = "Assets/Button_Red_Up.png"
        
        try:
            new_name = self.ids.IC_Blueprint_Name.text
            image_name = self.ids.IC_S.text
            
            if not image_name:
                raise ValueError("未选择图像")
            
            path_i = os.path.join(image_folder_path, image_name)
            color_tex = self.ids.IC_Color_Tex.text
            part_type = self.ids.IC_Type.text  # 已经是英文
            logo_width = float(self.ids.IC_Width.text)
            app_mod = self.ids.IC_Mono.text  # 需要判断中文
            
            # 创建蓝图结构
            delta = {
                "center": 9.0,
                "offset": {"x": 0.0, "y": 0.0},
                "parts": [],
                "stages": []
            }
            
            # 适配中文颜色模式
            if app_mod == "单色":
                with Image.open(path_i) as im:
                    rgb_im = im.convert("RGB")
                    height = logo_width / im.size[0]
                    
                    for y in range(im.size[1]):
                        count = 0
                        for x in range(im.size[0]):
                            pixel = rgb_im.getpixel((x, y))
                            
                            # 检查像素是否不是透明或白色
                            is_opaque = True
                            if len(pixel) > 3 and pixel[3] == 0:  # 透明
                                is_opaque = False
                            elif pixel[0] >= 240 and pixel[1] >= 240 and pixel[2] >= 240:  # 接近白色
                                is_opaque = False
                            
                            if is_opaque:
                                count += 1
                            else:
                                if count > 0:
                                    # 创建部件
                                    new_part = {
                                        "n": part_type,
                                        "p": {"x": (x - count/2) * height, "y": -(y + 0.5) * height + im.size[1] * height},
                                        "o": {"x": 1.0, "y": 1.0, "z": 270.0},
                                        "t": "-Infinity",
                                        "N": {},
                                        "T": {"color_tex": color_tex, "shape_tex": "Flat"}
                                    }
                                    
                                    if part_type == "Fairing":
                                        new_part["N"]["width_original"] = max(height - 0.4, 0.1)
                                        new_part["N"]["width_a"] = max(height - 0.4, 0.1)
                                        new_part["N"]["width_b"] = max(height - 0.4, 0.1)
                                        new_part["N"]["height"] = height * count
                                        new_part["T"]["fragment"] = "1"
                                        new_part["B"] = {"occupied_a": False}
                                    else:
                                        new_part["N"]["width_original"] = height
                                        new_part["N"]["width_a"] = height
                                        new_part["N"]["width_b"] = height
                                        new_part["N"]["height"] = height * count
                                    
                                    delta["parts"].append(new_part)
                                    count = 0
                        
                        # 处理行尾
                        if count > 0:
                            new_part = {
                                "n": part_type,
                                "p": {"x": (im.size[0] - count/2) * height, "y": -(y + 0.5) * height + im.size[1] * height},
                                "o": {"x": 1.0, "y": 1.0, "z": 270.0},
                                "t": "-Infinity",
                                "N": {},
                                "T": {"color_tex": color_tex, "shape_tex": "Flat"}
                            }
                            
                            if part_type == "Fairing":
                                new_part["N"]["width_original"] = max(height - 0.4, 0.1)
                                new_part["N"]["width_a"] = max(height - 0.4, 0.1)
                                new_part["N"]["width_b"] = max(height - 0.4, 0.1)
                                new_part["N"]["height"] = height * count
                                new_part["T"]["fragment"] = "1"
                                new_part["B"] = {"occupied_a": False}
                            else:
                                new_part["N"]["width_original"] = height
                                new_part["N"]["width_a"] = height
                                new_part["N"]["width_b"] = height
                                new_part["N"]["height"] = height * count
                            
                            delta["parts"].append(new_part)
            
            elif app_mod == "自动":
                colors = [
                    'Color_White',
                    'Color_Gray', 
                    'Color_Orange',
                    'Color_Black',
                    'Array',
                    'Gold_Foil'
                ]
                
                with Image.open(path_i) as im:
                    rgb_im = im.convert("RGB")
                    px = rgb_im.load()
                    height = logo_width / im.size[0]
                
                # 为每种颜色创建部件
                for color_tex in colors:
                    for y in range(im.size[1]):
                        count = 0
                        for x in range(im.size[0]):
                            pixel_color = getcolorfunc(px[x, y])
                            
                            if pixel_color == color_tex:
                                count += 1
                            else:
                                if count > 0:
                                    # 创建部件
                                    new_part = {
                                        "n": part_type,
                                        "p": {"x": (x - count/2) * height, "y": -(y + 0.5) * height + im.size[1] * height},
                                        "o": {"x": 1.0, "y": 1.0, "z": 270.0},
                                        "t": "-Infinity",
                                        "N": {},
                                        "T": {"color_tex": color_tex, "shape_tex": "Flat"}
                                    }
                                    
                                    if part_type == "Fairing":
                                        new_part["N"]["width_original"] = max(height - 0.4, 0.1)
                                        new_part["N"]["width_a"] = max(height - 0.4, 0.1)
                                        new_part["N"]["width_b"] = max(height - 0.4, 0.1)
                                        new_part["N"]["height"] = height * count
                                        new_part["T"]["fragment"] = "1"
                                        new_part["B"] = {"occupied_a": False}
                                    else:
                                        new_part["N"]["width_original"] = height
                                        new_part["N"]["width_a"] = height
                                        new_part["N"]["width_b"] = height
                                        new_part["N"]["height"] = height * count
                                    
                                    delta["parts"].append(new_part)
                                    count = 0
                        
                        # 处理行尾
                        if count > 0:
                            new_part = {
                                "n": part_type,
                                "p": {"x": (im.size[0] - count/2) * height, "y": -(y + 0.5) * height + im.size[1] * height},
                                "o": {"x": 1.0, "y": 1.0, "z": 270.0},
                                "t": "-Infinity",
                                "N": {},
                                "T": {"color_tex": color_tex, "shape_tex": "Flat"}
                            }
                            
                            if part_type == "Fairing":
                                new_part["N"]["width_original"] = max(height - 0.4, 0.1)
                                new_part["N"]["width_a"] = max(height - 0.4, 0.1)
                                new_part["N"]["width_b"] = max(height - 0.4, 0.1)
                                new_part["N"]["height"] = height * count
                                new_part["T"]["fragment"] = "1"
                                new_part["B"] = {"occupied_a": False}
                            else:
                                new_part["N"]["width_original"] = height
                                new_part["N"]["width_a"] = height
                                new_part["N"]["width_b"] = height
                                new_part["N"]["height"] = height * count
                            
                            delta["parts"].append(new_part)
            
            # 创建蓝图目录
            name_addition = 0
            original_new_name = new_name
            path = os.path.join(bp_folder_path, str(new_name))
            path_2_b = os.path.join(path, "Blueprint.txt")
            path_2_v = os.path.join(path, "Version.txt")
            
            while True:
                try:
                    os.mkdir(path)
                    break
                except FileExistsError:
                    name_addition += 1
                    new_name = f"{original_new_name} {name_addition}"
                    path = os.path.join(bp_folder_path, str(new_name))
                    path_2_b = os.path.join(path, "Blueprint.txt")
                    path_2_v = os.path.join(path, "Version.txt")
            
            # 写入文件
            with open(path_2_v, "w+") as v:
                v.write("1.5.2.5")
            
            with open(path_2_b, "w+") as f:
                json.dump(delta, f, indent=2)
                
        except (FileNotFoundError, ValueError, KeyError, IsADirectoryError, AttributeError) as e:
            self.ids.IC_Gen.text = "检查输入"
            self.ids.IC_Gen.background_normal = "Assets/Button_Orange_Up.png"
        except Exception as e:
            self.ids.IC_Gen.text = "错误"
            self.ids.IC_Gen.background_normal = "Assets/Button_Orange_Up.png"


class SFSToolsApp(App):
    def build(self):
        self.icon = "Assets/Icon.png"
        app = WindowManager()
        return app

    def on_pause(self):
        return True

    def on_start(self):
        # 确保目录存在
        for folder in [path_alpha, bp_folder_path, font_folder_path, image_folder_path]:
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception:
                pass


if __name__ == "__main__":
    SFSToolsApp().run()