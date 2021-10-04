#!/usr/bin/env python

import os, json


def checkfiles(root_path):
    valid_file = ['cuh', 'hh', 'cxx', 'cpp', 'c', 'h++', 'cu', 'hpp', 'hxx', 'c++', 'cc', 'h']
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):  # not a dir
            str = os.path.splitext(file)[-1][1:]
            if str not in valid_file and str != 'json':
                print(root_path, file + 'is not valid')
                os.remove(root_path + '/' + file)
                print('Delete' + root_path + '/' + file)
        else:
            checkfiles(root_path + '/' + file)


def get_file(root_path, all_files):
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):  # not a dir
            all_files.append(root_path + '/' + file)
        else:  # is a dir
            get_file((root_path + '/' + file), all_files)
    return all_files


def cpplint():
    output_list = ['vs7', 'emacs']
    level_list = ['1', '2', '3', '4', '5']
    counting_list = ['total', 'toplevel', 'detailed']
    root = '/home/test/'
    config_json = root + "cpplint.json"
    json_file_path = root + "cpplint_overviews.json"
    project_name = ''
    paras = ''
    root_dir = ''
    with open(config_json, 'r') as json_file:
        configure = json.load(json_file)
        flag = True
        for val in configure:
            if flag:
                project_name = val["project_name"]
                flag = False
            else:
                if val["name"] == "--verbose" and val["attr"] in level_list:
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                if val["name"] == "--output" and val["attr"] in output_list:
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                if val["name"] == "--counting" and val["attr"] in counting_list:
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                if val["name"] == "srcpath":
                    root_dir = val["attr"]
    #checkfiles(root_dir)
    paths = get_file(root, [])
    print("==========begin of cpplint check==========")
    print("The number of files:", len(paths))
    for path in paths:
        str = "cpplint %(paras)s %(path)s >> cpplint.txt 2>&1" % {'paras': paras, 'path': path}
        print("===path===", path)
        os.system(str)
    command = "./result_file.sh"
    print(command)
    os.system(command)
    print("==========end of cpplint check==========")
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        data['project'] = {"project_name": project_name, "tool_name": "cpplint"}
    with open(json_file_path, 'w') as json_file:
        json_file.write(json.dumps(data, indent=2))


if __name__ == '__main__':
    cpplint()
