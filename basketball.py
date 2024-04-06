from ursina import *
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader as lit
from random import uniform
import time
from effect import *

Entity.default_shader = basic_lighting_shader

balls = []
def input(key):
    print(key)
    if key == "c":
        print(cam.position, cam.rotation)

    # change dragging direction
    if key == "right mouse down":
        if ball.direction == "xz":
            ball.direction = "xy"
            ball.plane_direction = (0,0,1)
            ball.lock = (0,0,1)
        else:
            ball.direction = "xz"
            ball.plane_direction = (0,1,0)
            ball.lock = (0,1,0)

    # shooting
    if key == "space":
        if len(balls) > 0: return
        dir = ball.forward + Vec3(0, 0.3, 0)
        pos = ball.position #+ player.forward + Vec3(0,1,0)
        ball1 = Entity(model="basketball0.obj", texture = "uv_try.png",scale=1, color=color.white, position=pos, dir=dir)
        balls.append(ball1)
        ball.visible = False
    
    # animation
    if key == "a up":
        ball.anim = True
        invoke(setattr, ball, "anim", False, delay=8)
        ball.animate_position(cloth_right.position+Vec3(0,0.3,0), duration=3, curve=curve.linear)
        
        # ball animations
        invoke(setattr, ball, "visible", False, delay=3.2)
        invoke(setattr, ball, "visible", True, delay=8)
        invoke(setattr, ball, "position", Vec3(0,3,0), delay=8)
        
        # basket animation events
        invoke(basket_anim.start, delay=3)
        invoke(setattr, basket_anim, "visible", True, delay=3.2)
        invoke(setattr, basket_anim, "visible", False, delay=8)

        # cloth right events
        invoke(setattr, cloth_right, "visible", False, delay=3.2)
        invoke(setattr, cloth_right, "visible", True, delay=8)
        
        
def update():
    print(basket_anim.current_frame.model)
    # after shooting
    for ball1 in balls:
        ball1.position += ball1.dir * 30 * time.dt
        ball1.dir.y += (-.3 * time.dt)
        p = ParticleEmitter(position=ball1.position, file=r'effects\fire_sphere.ptf', life=3, deathtime=3)
        p.scale = .8

        if ball1.y < 0: 
            balls.remove(ball1)
            destroy(ball1)
            # ball new position
            ball.x = uniform(-8,8)
            ball.y = uniform(3,8)
            ball.z = 0
            ParticleEmitter(position=ball.position, file=r'effects\smoke.ptf', life=3, deathtime=3)
            ball.visible = True
            ball.limit = ball.x

    # prevent going forward
    if not ball.dragging:
        if ball.anim: return
        if ball.z > ball.limit: ball.z = ball.limit

app = Ursina(borderless=False)

ground = Entity(model="plane", position=Vec3(0,0,0), scale=300, texture="shore", collider="box")

basket_anim = FrameAnimation3d("basket_cloth_last/basket_cloth_", texture="uv_try.png", autoplay=False, visible = False, loop=False)
basket_anim.position = Vec3(0.050288, 10.463, 43.6884) # Vec3(0.010001, 10.463, 45.0088)           

court = Entity(model="court", position=Vec3(0,0,0), visible=True) # texture="uv_try.png",

cloth_right = Entity(model="cloth_object.obj", texture="uv_try.png", position=Vec3(0.050288, 10.463, 43.6884), visible=True) # Vec3(0, -2.9601, 41.4001)  

cloth_left = Entity(model="cloth_object.obj", texture="uv_try.png", position=Vec3(0.050288, 10.463, -43.6884), visible=True)

cam = EditorCamera(position=Vec3(-0.103426, 2.41059, 0.104484), rotation=Vec3(-0.915758, -0.977218, 0))
# sf = cam.add_script(SmoothFollow(target=ball, offset=(0,0.5,-4)))

ball = Draggable(parent=scene, model="basketball0.obj", texture = "uv_try.png", y=3, color=color.white, plane_direction=(0,1,0), lock = (0,1,0), direction="xz", limit=0, anim=False)

Sky()

app.enableParticles()
app.run()

# Basketball court by Poly by Google [CC-BY] via Poly Pizza
# Vcc3(0.010001, 10.463, 45.0088)