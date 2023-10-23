import bpy
import os, sys
import pandas as pd

def readfiles(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.fbx':
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    
    return file_list

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    fbx_list = readfiles(input_dir)
    df2list = []
    for fbx_path in fbx_list[:3]:
        filename = os.path.split(fbx_path)[-1]
        bpy.ops.import_scene.fbx(filepath=fbx_path)


        # dict for mesh:object[]
        mesh_objects = {}
        # create dict with meshes
        for m in bpy.data.meshes:
            mesh_objects[m.name] = []
        print(mesh_objects)
        
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
    #     # attach objects to dict keys
    #     for o in bpy.context.scene.objects:
    #         # only for meshes
    #         if o.type == 'MESH':
    #             # if this mesh exists in the dict
    #             if o.data.name in mesh_objects:
    #                 # object name mapped to mesh
    #                 # mesh_objects[o.data.name].append(o.name)
    #                 df2list.append([filename, o.data.name, o.name])

    # df = pd.DataFrame(df2list, columns=['file_name', 'index', 'object'])
    # df = df[df['index'] != 'Cube']
    # df.to_csv(f'{output_dir}/fbx_objects.csv', index=False)