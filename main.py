import os
import trimesh


class Voxelizer:
    def __init__(self, voxel_size=0.3):
        self.voxel_size = voxel_size

    def find_obj_models(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        obj_files = [os.path.join(current_dir, file) for file in os.listdir(current_dir) if file.endswith(".obj")]
        return obj_files

    def copy_mtl_file(self, original_obj_path, new_obj_path):
        # Пытаемся найти исходный .mtl файл, связанный с OBJ моделью
        original_mtl_path = original_obj_path.replace('.obj', '.mtl')
        if not os.path.exists(original_mtl_path):
            print(f"No .mtl file found for {original_obj_path}")
            return

        # Создаем новый .mtl файл на основе исходного
        new_mtl_path = new_obj_path.replace('.obj', '.mtl')
        with open(original_mtl_path, 'r') as original_mtl, open(new_mtl_path, 'w') as new_mtl:
            for line in original_mtl:
                # Здесь можно добавить логику для модификации свойств материалов
                new_mtl.write(line)

        print(f"New .mtl file created at {new_mtl_path}")
        return new_mtl_path

    def model_to_voxel(self):
        obj_paths = self.find_obj_models()
        if not obj_paths:
            print("No OBJ models found in the directory.")
            return

        for obj_path in obj_paths:
            mesh = trimesh.load(obj_path, process=False)
            voxel_grid = mesh.voxelized(pitch=self.voxel_size)
            voxel_mesh = voxel_grid.as_boxes()

            base_name = os.path.splitext(os.path.basename(obj_path))[0]
            voxelized_model_path = os.path.join(os.path.dirname(obj_path), f'{base_name}_voxelmodel.obj')

            voxel_mesh.export(voxelized_model_path)

            # Обновляем .mtl файл для новой модели
            new_mtl_path = self.copy_mtl_file(obj_path, voxelized_model_path)

            if new_mtl_path:
                # Если .mtl файл создан, обновляем .obj файл, чтобы он ссылался на новый .mtl
                with open(voxelized_model_path, 'a') as voxelized_obj:
                    voxelized_obj.write(f'\nmtllib {os.path.basename(new_mtl_path)}')

            print(f"Voxelized model saved to {voxelized_model_path}")


# Пример использования
voxelizer = Voxelizer(voxel_size=0.3)
voxelizer.model_to_voxel()
