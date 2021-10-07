#!/usr/bin/env python

import os, json

def transfer_toJson(path,output_path):
    result=dict()
    data=[]
    with open(path) as file:
        for line in file:
            tmp = dict()
            if line=='\n':
                break
            elif line[0]=='/':
                line=line.strip('\n')
                tmp['file_name']=line.split('(')[0].replace('/home/test/','')
                tmp['start']=line.split('(')[1].split(')')[0]
                tmp['type']=line.split('[')[1].split(']')[0]
                tmp['desc'] = line.split('[')[1].split(']')[1].strip('\t')
                tmp['level'] = line.split('[')[-1].split(']')[0].strip('\t')
                data.append(tmp)
    result['error']=data
    with open(output_path, 'w') as json_file:
        json_file.write(json.dumps(result, indent=2))

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
    output_list=['vs7','emacs']
    level_list = ['1', '2', '3', '4', '5']
    counting_list = ['total', 'toplevel', 'detailed']
    _ERROR_CATEGORIES = [
        'build/class',
        'build/c++11',
        'build/deprecated',
        'build/endif_comment',
        'build/explicit_make_pair',
        'build/forward_decl',
        'build/header_guard',
        'build/include',
        'build/include_alpha',
        'build/include_order',
        'build/include_what_you_use',
        'build/namespaces',
        'build/printf_format',
        'build/storage_class',
        'legal/copyright',
        'readability/alt_tokens',
        'readability/braces',
        'readability/casting',
        'readability/check',
        'readability/constructors',
        'readability/fn_size',
        'readability/function',
        'readability/inheritance',
        'readability/multiline_comment',
        'readability/multiline_string',
        'readability/namespace',
        'readability/nolint',
        'readability/nul',
        'readability/strings',
        'readability/todo',
        'readability/utf8',
        'runtime/arrays',
        'runtime/casting',
        'runtime/explicit',
        'runtime/int',
        'runtime/init',
        'runtime/invalid_increment',
        'runtime/member_string_references',
        'runtime/memset',
        'runtime/indentation_namespace',
        'runtime/operator',
        'runtime/printf',
        'runtime/printf_format',
        'runtime/references',
        'runtime/string',
        'runtime/threadsafe_fn',
        'runtime/vlog',
        'whitespace/blank_line',
        'whitespace/braces',
        'whitespace/comma',
        'whitespace/comments',
        'whitespace/empty_conditional_body',
        'whitespace/empty_loop_body',
        'whitespace/end_of_line',
        'whitespace/ending_newline',
        'whitespace/forcolon',
        'whitespace/indent',
        'whitespace/line_length',
        'whitespace/newline',
        'whitespace/operators',
        'whitespace/parens',
        'whitespace/semicolon',
        'whitespace/tab',
        'whitespace/todo',
    ]
    root = '/home/test/'
    config_json = root + "cpplint.json"
    json_file_path = root + "cpplint_overviews.json"
    project_name = ''
    paras = ''
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
                if val["name"] == "--linelength":
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                if val["name"] == "--counting" and val["attr"] in counting_list:
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                if val["name"] == "--output" and val["attr"] in output_list:
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                '''if val["name"] == "--headers":
                    paras = paras + val["name"] + "=" + val["attr"] + ' '
                if val["name"] == "--filter":
                    paras = paras + val["name"] + "=" + val["attr"] + ' ' '''

    paths = get_file(root, [])
    print("==========begin of cpplint check==========")
    print("The number of files:", len(paths))
    for path in paths:
        str = "cpplint %(paras)s %(path)s >> cpplint.txt 2>&1" % {'paras': paras, 'path': path}
        print("===path===", path)
        os.system(str)
    command='./result_file.sh'
    os.system(command)
    transfer_toJson("./cpplint.txt",json_file_path)
    print("==========end of cpplint check==========")
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        data['project'] = {"project_name": project_name, "tool_name": "cpplint"}
    with open(json_file_path, 'w') as json_file:
        json_file.write(json.dumps(data, indent=2))


if __name__ == '__main__':
    cpplint()
