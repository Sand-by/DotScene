import moderngl_window as mglw
import imgui
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from pathlib import Path

class App(mglw.WindowConfig):
    window_size = 1280,720
    vsync = True
    aspect_ratio  = 16/9
    resizable = False
    resource_dir = (Path(__file__).parent / 'shaders').resolve()
    title = 'FlyingDots'
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.pause = False
        self.show = False
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)
        self.agent_config = TextureConfig()
        self.agent_config.spesd = 1.0
        self.agent_config.count = 1.0

        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(vertex_shader='vertex.glsl',fragment_shader='fragment.glsl')
        self.set_uniform('resolution',self.window_size)
        mglw.window().fullscreen_key = mglw.window().keys.F

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))
        self.set_uniform('resolution',(width,height))

    def set_uniform(self,u_name,u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform:{u_name} - not used in shader')

    def render(self, time: float, frame_time):
        if not self.pause:
            self.set_uniform('time',time)

        self.set_uniform('is',self.show)
        self.set_uniform('speed',self.agent_config.spesd)
        self.set_uniform('part_count',self.agent_config.count)
        self.ctx.clear(1.0,1.0,1.0)
        self.set_uniform('color_1',TextureConfig.color_1)
        self.set_uniform('color_2',TextureConfig.color_2)

        self.quad.render(self.prog)
        self.imgui_newFrame()
        self.imgui_render()

    def imgui_newFrame(self):
        imgui.new_frame()
        imgui.begin("Properties", True)
        c, self.pause = imgui.checkbox("Paused", self.pause); imgui.same_line(spacing=50)
        c, self.show = imgui.checkbox("Show", self.show)
        
        imgui.spacing();imgui.spacing();imgui.separator();imgui.spacing();imgui.spacing()

        imgui.text("Dots Settings"); imgui.spacing()
        imgui.begin_group()
        c, TextureConfig.color_1 = imgui.color_edit3("Color 1", *TextureConfig.color_1)
        c, TextureConfig.color_2 = imgui.color_edit3("Color 2", *TextureConfig.color_2)
        c, new_N = imgui.slider_float(
                    label="Speed",
                    value=self.agent_config.spesd,
                    min_value=0,
                    max_value=5,
                    format="%.2f")
        if c:
            self.agent_config.spesd = new_N
        c,self.agent_config.count = imgui.drag_float(label = "Count", 
                                                                value = self.agent_config.count, 
                                                                change_speed=1.0, 
                                                                min_value=1.0, 
                                                                max_value=30.0, 
                                                                format='%.f')
        imgui.end_group()
        imgui.spacing();imgui.spacing();imgui.separator();imgui.spacing();imgui.spacing()
        imgui.text("Press F for FullScreen"); imgui.spacing()
        imgui.end()

    def imgui_render(self):
        imgui.render()
        self.imgui.render(imgui.get_draw_data())   
    def key_event(self, key, action, modifiers):
    # Key presses
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
            # Using modifiers (shift and ctrl)
                print("Space was pressed")
            if key == self.wnd.keys.Z and modifiers.shift:
                print("Shift + Z was pressed")
            if key == self.wnd.keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")
        # Key releases 
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was released")
    # def unicode_char_entered(self, char: str):
    #     print('character entered:', char)
    
    def resize(self, width: int, height: int):
        self.imgui.resize(width, height)
        self.set_uniform('resolution',(width,height))

    # def key_event(self, key, action, modifiers):
    #     self.imgui.key_event(key, action, modifiers)

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

class TextureConfig:
	color_1 = (1.0, 1.0, 0)
	color_2 = (1.0, 0.0, 1.0)
	color_3 = (0, 1, 0)
	spesd = 1.0
	count = 1.
	
if __name__ == '__main__':
    mglw.run_window_config(App)