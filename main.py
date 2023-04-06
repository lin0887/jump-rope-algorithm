import post
import counter
import os

if os.path.isdir('..\\output\\') != True:
    os.system("mkdir {}".format('..\\output\\'))
    print("create folder: {}".format('..\\output\\'))

files = os.listdir('..\\input\\')

for file in files:
    
    input_path = '..\\input\\'+file
    output_path = '..\\output\\'+file
    
    student = post.Post_dection(input_path)
    post_df = student.dection()

    a = counter.Body_point(post_df)
    for i in range(2):
        a.get_amplitude()
        a.get_wavelength()
        
    ans = a.jump_rope_count()  
    print('\ntime :{}\n'.format(ans))
    f = a.make_flag()

    student.make_output_vidoe(output_path,f)

