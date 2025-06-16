import os;import sys;import cv2;import numpy as np;from cores import options;from util import clean,mseeker;from PIL import Image

# ------------------Get Options------------------
opt=options();opt.parser.add_argument('-f',type=str,default='./file.mp4',help='loaction of file');opt.parser.add_argument('-p',type=str,default='./3]models/pretrained/1.pth',help='position seeker ai');opt=opt.getparse();print(f'[Options: ---------------]\nfile: {opt.f}\nposition: {opt.p}\n]------------------------[')


# ---------------Video To Image------------------
def video_to_frames(video_path,output_folder,prefix="frame",ext="png"):os.makedirs(output_folder,exist_ok=True);cap=cv2.VideoCapture(video_path);[cv2.imwrite(os.path.join(output_folder,f"{prefix}_{i:05d}.{ext}"),f)for i,(r,f)in enumerate(iter(cap.read,(False,None)))if r];cap.release()
video_extensions=('.mp4','.avi','.mov','.mkv','.webm','.flv','.wmv','.mpeg');video_to_frames(opt.f,'dataset/tmp')if opt.f.lower().endswith(video_extensions)else print("Video not detected, tracer will not work without moving mosiac areas!\nResorting to images for mosiac findings")


# --------------Image Processing-----------------
mseeker.test(opt.f)





# cleanup
print('[Cleaning all cache: --------------------------------------]');clean.cleanall();print(']----------------------------------------------------------[')
#If your here to learn code - im sorry, if your here to fix things - im sorry, if your here to use then dont worry about the code.  also im not sorry i went through hell making this
