import os 
import sys
import shutil
import json 
from subprocess import run, PIPE



DIR_WORD = "game"
CODE_EXTENSION = ".go"
COMPILE_COMMAND = ["go", "build"]



#  getting all game directories from the source directory
def find_all_game_paths(source):
    game_paths = []

    for root , dirs,files in os.walk(source):
        for directory in dirs:
            if DIR_WORD in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break
    return game_paths


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)




# code to copy and overwrite the destination directory
def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data, f)




# Down code is to complile the game code 

def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(CODE_EXTENSION):
                code_file_name = file
                break
        break

    # if no files found so return here we are compiling go programming files 
    if code_file_name is None:
        return 
    
    command = COMPILE_COMMAND + [code_file_name]
    run_command(command, path)



def run_command(command, path):

    # here we need to change from python running directory to all games command directory so that we can run files and again we will come back to original path 
    current_path = os.getcwd()

    os.chdir(path)
    result = run(command, stdout=PIPE, stderr=PIPE,universal_newlines=True)
    print("compile result",result)
    os.chdir(current_path)












#  Below is Main code and systems


def main(source,target):
    # current working directory 
    path = os.getcwd()

    source_path = os.path.join(path,source)
    target_path = os.path.join(path,target)

    game_files_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_files_paths, "_game")

    create_dir(target_path)

    for src,dest in zip(game_files_paths, new_game_dirs):
        dest_path = os.path.join(target_path,dest)
        copy_and_overwrite(src,dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "game_metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)



if __name__ == "__main__": 
    args = sys.argv
    if len(args)!=3:
        raise Exception("need to pass source and target <source> <target> directory only")
    
    source,target = args[1:]
    main(source, target)


