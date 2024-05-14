import os
import Mesh
import MeshPart
import re
 
# 現在のフォルダ
doc = App.ActiveDocument
PWD = re.findall("(.*)/",doc.FileName)[0]
print('現在のフォルダ：',PWD)
print( re.findall("(.*)/",doc.FileName))
labels = []
 
for obj in doc.Objects:
  print(obj)
  if obj.Visibility == True:
      mesh = doc.addObject("Mesh::Feature", "Mesh")
      print(mesh)
      mesh.Mesh = Mesh.Mesh(obj.Shape.tessellate(0.01))
      print(mesh.Mesh)
 
      label = obj.Label[:]
      labels.append(label)
      Mesh.export([mesh], fr'{PWD}/{label}.ast')
      print(label)
      doc.removeObject(mesh.Name)
          
print(doc.Label)
print(labels, type(labels))
 
with open(rf'{PWD}/{doc.Label}.stl', 'w') as f:
    print('test')
    for label in labels:
        with open(rf'{PWD}/{label}.ast', 'r') as fi:
            for line in fi:
                if line[:5] == 'solid':
                    line = 'solid ' + label + '\n'
                elif line[:8] == 'endsolid':
                    line = 'endsolid ' + label + '\n'
                f.write(line)
 
for label in labels:
    os.remove(rf'{PWD}/{label}.ast')
