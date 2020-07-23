import struct
from obj import ObjFile

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([round(b * 255), round(g * 255), round(r * 255)])

BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)

class Render(object):
    def __init__(self, w, h):
        self.glInit(w, h)
    
    # no tiene parámetros
    # esta función se ejecuta al crear un objeto de tipo render
    # inicializa las variables necesarias en su valor default
    def glInit(self, width, height):
        self.height = 0
        self.width = 0
        self.vp_height = 0
        self.vp_width = 0
        self.vp_start_point_x = 0
        self.vp_start_point_y = 0
        self.clear_color = BLACK
        self.point_color = WHITE
        self.glCreateWindow(width, height)

    # (width, height)
    # se inicializa el framebuffer con la altura y ancho indicados
    def glCreateWindow(self, width, height):
        self.height = round(height)
        self.width = round(width)
        self.glClear()
        self.glViewPort(0, 0, width, height)
        
        return True

    # no tiene parametros
    # se llena el mapa de bits con el color seleccionado
    def glClear(self):
        self.pixels = [[self.clear_color for x in range(self.width)] for y in range(self.height)]

    # (r, g, b) - valores entre 0 y 1
    # define el color con el que se realiza el clear
    def glClearColor(self, r, g, b):
        if r > 1 or r < 0 or g > 1 or g < 0 or b > 1 or b < 0:
            return False
        
        self.clear_color = color(r, g, b)
        return True
    
    # (r, g, b) - valores entre 0 y 1
    # define el color con el que se dibuja el punto
    def glColor(self, r, g, b):
        if r > 1 or r < 0 or g > 1 or g < 0 or b > 1 or b < 0:
            return False

        self.point_color = color(r, g, b)
        return True

    # (x, y, width, height)
    # crea el viewport en donde se podrá dibujar
    # restringe al viewport dentro de la ventana
    def glViewPort(self, x, y, width, height):
        if x > self.width or y > self.height:
            return False
        elif x + width > self.width or y + height > self.height:
            return False
        else:
            self.vp_start_point_x = x
            self.vp_start_point_y = y
            self.vp_width = width
            self.vp_height = height
            return True

    # no tiene parámetros
    # función extra
    # dibuja el contorno del viewport 
    def glDrawViewPort(self):
        for x in range(self.vp_start_point_x, self.vp_start_point_x + self.vp_width):
            self.pixels[self.vp_start_point_y][x] = color(255, 0, 251)
            self.pixels[self.vp_start_point_y + self.vp_height][x] = color(255, 0, 251)
        
        for y in range(self.vp_start_point_y, self.vp_start_point_y + self.vp_height):
            self.pixels[y][self.vp_start_point_x] = color(255, 0, 251)
            self.pixels[y][self.vp_start_point_x + self.vp_width] = color(255, 0, 251)

    # (x, y) - valores entre -1 y 1
    # se crea un punto dentro del viewport
    # las coordenadas son relativas al viewport
    def glVertex(self, x, y):
        if x > 1 or x < -1 or y > 1 or y < -1:
            return False
        else:
            new_x = (x + 1) * (self.vp_width / 2) + self.vp_start_point_x
            new_y = (y + 1) * (self.vp_height / 2) + self.vp_start_point_y
            self.pixels[round(new_y - 1) if round(new_y) == self.vp_height else round(new_y)][round(new_x - 1) if round(new_x) == self.vp_width else round(new_x)] = self.point_color

            return True

    # (x, y) - coordenadas
    # recibe las coordenadas en pixeles para dibujar 
    def glVertexNDC(self, x, y):
        self.pixels[(y - 1) if y == self.vp_height else y][(x - 1) if x == self.vp_width else x] = self.point_color
    
    # (x0, y0, x1, y1) - el punto inicial y final de una recta
    # la función es una implementación del algoritmo de bresenham
    # permite dibujar una linea de un punto inicial a uno final (en coordenadas relativas al vp entre -1 y 1)
    def glLine(self, x0, y0, x1, y1):
        new_x0 = round((x0 + 1) * (self.vp_width / 2) + self.vp_start_point_x)
        new_y0 = round((y0 + 1) * (self.vp_height / 2) + self.vp_start_point_y)
        new_x1 = round((x1 + 1) * (self.vp_width / 2) + self.vp_start_point_x)
        new_y1 = round((y1 + 1) * (self.vp_height / 2) + self.vp_start_point_y)

        ystep = False

        if abs(new_x1 - new_x0) < abs(new_y1 - new_y0):
            ystep = True
            new_x0, new_x1, new_y0, new_y1 = new_y0, new_y1, new_x0, new_x1

        if (new_x0 > new_x1):
            new_x0, new_x1, new_y0, new_y1 = new_x1, new_x0, new_y1, new_y0

        dx = new_x1 - new_x0
        dy = new_y1 - new_y0

        xsign = 1
        ysign = 1

        if dy < 0:
            ysign = -1
            dy = -dy

        D = 2 * dy - dx
        Y = new_y0

        for x in range(new_x0, new_x1):
            if ystep:
                self.glVertexNDC(Y, x)
            else:
                self.glVertexNDC(x, Y)

            if D > 0:
                Y = Y + ysign
                D = D - 2 * dx
            
            D = D + 2 * dy

    # (x0, y0, x1, y1) - el punto inicial y final de una recta
    # la función es una implementación del algoritmo de bresenham
    # permite dibujar una linea de un punto inicial a uno final (en coordenadas de la ventana)
    def glLineNDC(self, x0, y0, x1, y1):
        ystep = False

        if abs(x1 - x0) < abs(y1 - y0):
            ystep = True
            x0, x1, y0, y1 = y0, y1, x0, x1

        if (x0 > x1):
            x0, x1, y0, y1 = x1, x0, y1, y0

        dx = x1 - x0
        dy = y1 - y0

        xsign = 1
        ysign = 1

        if dy < 0:
            ysign = -1
            dy = -dy

        D = 2 * dy - dx
        Y = y0

        for x in range(x0, x1):
            if ystep:
                self.glVertexNDC(Y, x)
            else:
                self.glVertexNDC(x, Y)

            if D > 0:
                Y = Y + ysign
                D = D - 2 * dx
            
            D = D + 2 * dy

    def glObj(self, obj__file, translate, scale):
        model = ObjFile(obj__file)

        for face in model.faces:

            vertCount = len(face)

            for vert in range(vertCount):
                v0 = model.vertexes[ face[vert][0] - 1]
                v1 = model.vertexes[ face[(vert + 1) % vertCount][0] - 1]

                x0 = round(v0[0] * scale[0] + translate[0])
                y0 = round(v0[1] * scale[1] + translate[1])
                x1 = round(v1[0] * scale[0] + translate[0])
                y1 = round(v1[1] * scale[1] + translate[1])

                self.glLineNDC(x0, y0, x1, y1)

    # no tiene parámetros
    # renderiza el mapa de bits
    def glFinish(self):
        file = open('SR3.bmp', 'wb')

        # file header
        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))
                   
        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        # image header
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        # pixels, 3 bytes each
        for x in range(self.height):
            for y in range(self.width):
                file.write(self.pixels[x][y])

        file.close()
