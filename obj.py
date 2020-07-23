import re

# Clase para un archivo de tipo .obj
# Abre el archivo, lo lee, y luego separa los atributos en:
# Vertices, Normals, Textures y Faces
class ObjFile(object):
    
    # Inicializa el objeto
    # Se dividen las lineas del archivo y se guardan en una lista
    def __init__(self, filename):
        self.lines = []
        self.vertexes = []
        self.normals = []
        self.textures = []
        self.faces = []

        obj__file = open(filename, 'r')

        for line in obj__file.readlines():
            self.lines.append(line.split(maxsplit = 1))

        self.objRead()

    # Lee las lineas del archivo 
    # Separa cada atributo según sea V, VN, T, F
    def objRead(self):
        for line in self.lines:
            prefix, values = line[0], line[1]

            if prefix == 'v':
                self.vertexes.append(list(map(float, re.split(' ', values))))
            elif prefix == 'vn':
                self.normals.append(list(map(float, re.split(' ', values))))
            elif prefix == 'vt':
                self.textures.append(list(map(float, re.split(' ', values))))
            elif prefix == 'f':
                face = []
                for vert in re.split(' ', values):
                    face.append(list(map(int, re.split('/', vert))))
                    
                self.faces.append(face)

