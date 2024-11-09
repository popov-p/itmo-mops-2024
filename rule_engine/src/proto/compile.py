import os
import subprocess
import glob

def compile_protobuf():
    proto_dir = os.path.join(os.getcwd(), 'src', 'proto')
    proto_files = glob.glob(os.path.join(proto_dir, '*.proto'))

    if not proto_files:
        raise FileNotFoundError(f"No .proto files found in {proto_dir}")

    for file in proto_files:
        try:
            os.chmod(file, 0o644)
        except Exception as e:
            print(f"Error changing permissions for {file}: {e}")
    
    command = [
        "protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={proto_dir}"
    ] + proto_files
    
    try:
        subprocess.run(command, check=True)
        print("Protobuf message modules successfully generated!")
    except subprocess.CalledProcessError as e:
        print(f"Protobuf generation command failed with error code {e.returncode}")