import os;import shutil
def Traversal(filedir):return([os.path.join(r,f)for r,_,files in os.walk(filedir)for f in files],[os.path.join(r,d)for r,dirs,_ in os.walk(filedir)for d in dirs])
def cleanall():
    file_list, dir_list = Traversal('./')
    for file in file_list: [os.remove(file), print(f'remove file: {file}')][0] if ('tmp' in file or 'pycache' in file) and os.path.exists(file) and 'imgs' not in file else None
    [shutil.rmtree(dir) and print(f'remove dir: {dir}') for dir in dir_list if ('tmp' in dir or 'pycache' in dir) and os.path.exists(dir)]
#hehehehaw, this is cursed art
