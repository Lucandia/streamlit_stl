import os
import shutil
import atexit
import tempfile
import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))

class STLComponent:
    def __init__(self):
        """Initialize the STLComponent class and set up the environment."""
        self.has_setup = False
        self.temp_folder = None
        self.current_temp_files = []  # List to track created temporary files
        self.setup()  # Automatically call setup upon initialization

    def setup(self):
        """Set up the necessary directories for the Streamlit_stl component."""
        if not self.has_setup:
            # Create a unique temporary directory for the component
            if self.temp_folder and os.path.exists(self.temp_folder):
                shutil.rmtree(self.temp_folder)
            self.temp_folder = tempfile.mkdtemp(suffix='_st_stl')
            # Copy the current component directory to the temporary folder
            for file in os.listdir(parent_dir):
                src = parent_dir + os.sep + file
                dst = self.temp_folder + os.sep + file
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy(src, dst)
            self.has_setup = True  # Mark setup as complete to prevent re-initialization

    def stl_from_text(self, text, color='#696969', material='material', auto_rotate=False, height=500, **kwargs):
        """
        Create and manage temporary files for the given text configurations and pass them to the Stl component.

        Parameters:
        - text: Text of the stl file
        - color: The hexadecimal color (starting with '#')
        - material: The material of the stl file ('material' or 'wireframe')
        - height: Height of the component display
        """
        self.setup()  # Ensure the environment is set up
        file_path = []  # The path of the created temporary file
        if material not in ('material', 'wireframe'):
            raise ValueError(f'The possible materials are "material" or "wireframe", got {material} instead')
        if color[0] != '#':
            raise ValueError(f"The color must be a hexadecimal value starting with '#', got {color} instead")
        if text is not None:
            try:
                # Create a temporary file in the temporary stl folder
                with tempfile.NamedTemporaryFile(dir=self.temp_folder, suffix='.stl', delete=False) as temp_file:
                    if isinstance(text, bytes):
                        temp_file.write(text)
                    elif isinstance(text, str):
                        temp_file.write(text.encode("utf-8"))  # Write the text content to the file
                    else:
                        raise ValueError(f"Invalid text type for the stl file")
                    temp_file.flush()  # Ensure all data is written to disk
                    file_path = temp_file.name.split(os.sep)[-1]  # Store the relative path
                    self.current_temp_files.append(temp_file.name)  # Keep track of the file for cleanup
            except Exception as e:
                print(f"Error processing the stl file: {e}")
                _component_func(files_text='', height=height **kwargs)
                return False
        # Call the stl component with the list of file paths and their types
        _component_func(file_path=file_path, color=color, material=material, auto_rotate=bool(auto_rotate), height=height, **kwargs)
        return True

    def stl_from_file(self, file_path=None, color='#696969', material='material', auto_rotate=False, height=500, **kwargs):
        """
        Read content from files and pass it to the stl_from_text function.

        Parameters:
        - file_path: The path to the stl file
        - color: The hexadecimal color (starting with '#')
        - material: The material of the stl file ('material' or 'wireframe')
        - height: Height of the component display
        """
        file_text = None
        if file_path is not None:
            with open(file_path, "rb") as f:
                file_text = f.read()  # Read the file content and add it to the list
        # Pass the file content to stl_from_text
        return self.stl_from_text(text=file_text, color=color, material=material, auto_rotate=auto_rotate, height=height, **kwargs)

    def cleanup_temp_files(self):
        """Clean up temporary files and directories created during the session."""
        try:
            if os.path.exists(self.temp_folder):
                shutil.rmtree(self.temp_folder)  # Remove the entire temporary directory
        except Exception as e:
            print(f"Error deleting temporary streamlit-stl folder {self.temp_folder}: {e}")
            # If the directory can't be deleted, try to delete each file individually
            for temp_file in self.current_temp_files:
                try:
                    os.unlink(temp_file)  # Remove individual temporary files
                except Exception as e:
                    print(f"Error deleting temp file {temp_file}: {e}")

# Instantiate the STLComponent class to set up the environment and handle resources
stl_component = STLComponent()
# Register the cleanup function to be called automatically when the program exits
atexit.register(stl_component.cleanup_temp_files)


### Declare the functions to be used in the Streamlit script
stl_from_text = stl_component.stl_from_text
stl_from_file = stl_component.stl_from_file

# Declare the Streamlit component and link it to the temporary directory
_component_func = components.declare_component(
    "streamlit_stl",
    path=stl_component.temp_folder,
)