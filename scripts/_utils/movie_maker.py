def movie_maker(resolution='1920:1080', images_directory='images', seconds_per_image=10, fade_duration=1, color_space='yuv420p', output_file='/tmp/slideshow.mp4'):
    import os

    #  https://superuser.com/questions/833232/create-video-with-5-images-with-fadein-out-effect-in-ffmpeg/834035#834035
    image_files = os.listdir(images_directory)
    num_images = len(image_files)

    fade_out = "fade=t=out:st={}".format(seconds_per_image - fade_duration)
    fade_in = "fade=t=in:st=0:d={}".format(fade_duration)
    fade_in_and_out = '{},{}'.format(fade_in, fade_out)

    # fade_in_cross = 'fade=d=1:t=in:alpha=1'

    frame_settings = 'scale={}:force_original_aspect_ratio=decrease,pad={}:(ow-iw)/2:(oh-ih)/2,setsar=1'.format(resolution, resolution)

    image_inputs = ''
    for image in image_files:
        # '-loop 1 -t 5 -i images/input0.png' 
        image_inputs += '-loop 1 -t {} -i {}{}{} '.format(seconds_per_image, images_directory, os.path.sep, image)

    # Create transition filter
    filter_complex = '-filter_complex "'
    for i, image in enumerate(image_files):
        # first image only fades out
        if i is 0:
            fade = fade_out
        else:
            fade = fade_in_and_out
        
        #Fade to black:
        filter_complex += '[{}:v]{},{}:d=1[v{}]; '.format(i, frame_settings, fade, i)
        #Crossfade:
        #filter_complex += f'[{i}:v]{frame_settings},[{i}]format=yuva444p,{fade}:d=1[v{i}]; '
        

    for i in range(num_images):
        filter_complex += '[v{}]'.format(i)  # [v0][v1][v2][v3][v4]concat=n=5

    filter_complex += 'concat=n={}:v=1:a=0,format={}[v]" -map "[v]" '.format(num_images, color_space)

    cmd = 'ffmpeg {} {} {}'.format(image_inputs, filter_complex, output_file)

    os.system(cmd)
