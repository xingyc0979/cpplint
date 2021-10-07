import json


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

if __name__ == '__main__':
    transfer_toJson("./cpplint.txt","overview.json")