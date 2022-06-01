import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader


vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(
        45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

# load here the 3d meshes
roof_indices, roof_buffer = ObjLoader.load_model("components/roof.obj")
seat_indices, seat_buffer = ObjLoader.load_model("components/seats.obj")
pitch_indices, pitch_buffer = ObjLoader.load_model("components/pitch.obj")
ground_indices, ground_buffer = ObjLoader.load_model("components/ground.obj")

shader = compileProgram(compileShader(
    vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))


# VAO and VBO
VAO = glGenVertexArrays(4)
VBO = glGenBuffers(4)
# EBO = glGenBuffers(1)

# ROOF

# roof VAO
glBindVertexArray(VAO[0])
# roof Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, roof_buffer.nbytes, roof_buffer, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, roof_indices.nbytes, roof_indices, GL_STATIC_DRAW)

# roof vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      roof_buffer.itemsize * 8, ctypes.c_void_p(0))
# roof textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      roof_buffer.itemsize * 8, ctypes.c_void_p(12))
# roof normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      roof_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


# SEATS

# seats VAO
glBindVertexArray(VAO[1])
# seats Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, seat_buffer.nbytes, seat_buffer, GL_STATIC_DRAW)
# seats vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      seat_buffer.itemsize * 8, ctypes.c_void_p(0))
# seats textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      seat_buffer.itemsize * 8, ctypes.c_void_p(12))
# seats normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      seat_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


# FIELD

# field VAO
glBindVertexArray(VAO[2])
# field Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, pitch_buffer.nbytes,
             pitch_buffer, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, roof_indices.nbytes, roof_indices, GL_STATIC_DRAW)

# field vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      pitch_buffer.itemsize * 8, ctypes.c_void_p(0))
# field textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      pitch_buffer.itemsize * 8, ctypes.c_void_p(12))
# field normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      pitch_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


# PLANE

# plane VAO
glBindVertexArray(VAO[3])
# field Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, ground_buffer.nbytes,
             ground_buffer, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, roof_indices.nbytes, roof_indices, GL_STATIC_DRAW)

# plane vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      ground_buffer.itemsize * 8, ctypes.c_void_p(0))
# plane textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      ground_buffer.itemsize * 8, ctypes.c_void_p(12))
# plane normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      ground_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


# TEXTURES

textures = glGenTextures(4)
load_texture("components/roof.jpg", textures[0])
load_texture("components/seats.jpg", textures[1])
load_texture("components/pitch2.jpg", textures[2])  # added
load_texture("components/ground.jpg", textures[3])  # added

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(
    45, 1280 / 720, 0.1, 100)
roof_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
seat_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
pitch_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([0, -5, -10]))  # added
ground_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([0, -5, -10]))  # added

# eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3(
    [0, 12, 8]), pyrr.Vector3([0, 0, -5]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    time = glfw.get_time()

    # # ROOF
    rot_y = pyrr.Matrix44.from_y_rotation(0.5 * time)
    model = pyrr.matrix44.multiply(rot_y, roof_pos)
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(roof_indices))
    # glDrawElements(GL_TRIANGLES, len(roof_indices), GL_UNSIGNED_INT, None)

    # SEATS
    rot_y = pyrr.Matrix44.from_y_rotation(0.5 * time)
    model = pyrr.matrix44.multiply(rot_y, seat_pos)
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(seat_indices))

    # PITCH
    rot_y = pyrr.Matrix44.from_y_rotation(0.5 * time)
    model = pyrr.matrix44.multiply(rot_y, pitch_pos)
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(pitch_indices))

    # GROUND
    rot_y = pyrr.Matrix44.from_y_rotation(0.5 * time)
    model = pyrr.matrix44.multiply(rot_y, ground_pos)
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(ground_indices))

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
