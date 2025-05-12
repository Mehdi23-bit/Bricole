def remove_gaps(gaped_str):
    sub_str=gaped_str.split()
    final=''
    for str in sub_str:
      final+=str

    return final

def extract_pictures(path,imgs_url):
   
   imgs=(imgs_url.strip()).split('*')
   imgs.remove('')
   
   for i,img in enumerate(imgs):
      imgs[i]=f"{path}{img}"
   
   return imgs 
   
   