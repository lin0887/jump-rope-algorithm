import post
import counter

input_path = '..\\input\\A1102.MOV'
output_path = '..\\output\\'+input_path.split('\\')[-1]
student = post.Post_dection(input_path)
post_df = student.dection()

a = counter.Body_point(post_df)
for i in range(2):
    a.get_amplitude()
    a.get_wavelength()
    
ans = a.jump_rope_count()  
print(ans)
f = a.make_flag()

student.make_output_vidoe(output_path,f)

