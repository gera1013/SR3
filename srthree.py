from obj import ObjFile
from gl import Render, color

r = Render(800, 600)

r.glObj('lowpolytree.obj', (400, 250), (100, 100))

r.glFinish()
