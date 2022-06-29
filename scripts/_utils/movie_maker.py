import os
import argparse
from PIL import Image


def movie_maker(resolution='1920:1080', images_directory='images', seconds_per_image=7, fade_duration=1, color_space='yuv420p', output_file='/tmp/slideshow.mp4'):
  
    #  https://superuser.com/questions/833232/create-video-with-5-images-with-fadein-out-effect-in-ffmpeg/834035#834035
    image_files = sorted(os.listdir(images_directory)) # want them alphabetical so title image comes first!

    if image_files:
        print("\nFound images: {}\n".format(image_files))
    else:
        print("\nNo images found in '{}'!  Quitting this...\n".format(images_directory))

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
        if i == 0:
            fade = fade_out
        else:
            fade = fade_in_and_out

        # Fade to black:
        filter_complex += '[{}:v]{},{}:d=1[v{}]; '.format(i, frame_settings, fade, i)
        # Crossfade:
        # filter_complex += f'[{i}:v]{frame_settings},[{i}]format=yuva444p,{fade}:d=1[v{i}]; '

    for i in range(num_images):
        filter_complex += '[v{}]'.format(i)  # [v0][v1][v2][v3][v4]concat=n=5

    filter_complex += 'concat=n={}:v=1:a=0,format={}[v]" -map "[v]" '.format(num_images, color_space)

    cmd = 'ffmpeg {} {} {}'.format(image_inputs, filter_complex, output_file)

    os.system(cmd)


if __name__ == "__main__":
    # execute only if run as a script

    parser = argparse.ArgumentParser(description='Generate a video file from a directory of images.')
    parser.add_argument('--images', type=str, help='directory to find the images ["images"]')
    parser.add_argument('--resolution', type=str, help='output video resolution ["1920:1080"]')
    parser.add_argument('--seconds', type=int, help='seconds per image [3]')
    parser.add_argument('--fade', type=int, help='fade duration between images [1]')
    parser.add_argument('--output', type=str, help='output file ["/tmp/slideshow.mp4"]')

    args = parser.parse_args()

    # If parameters are provided pass them to the function, otherwise defaults will be used.
    kwargs = {}
    if args.images:
        kwargs['images_directory']=args.images
    if args.resolution:
        kwargs['resolution']=args.resolution
    if args.seconds:
        kwargs['seconds_per_image']=args.seconds
    if args.fade:
        kwargs['fade_duration']=args.fade
    if args.output:
        kwargs['output_file']=args.output

    movie_maker(**kwargs)


def gif2mp4(path_to_gif):
    """ 
    Convert an animated gif to mp4 via ffmpeg.  
    Return False if the conversion fails, otherwise returns the path to the new mp4
    """

    im = Image.open(path_to_gif)
    if not im.is_animated:
        print(f"GIF to MP4 conversion failed. This is not an animated gif: {path_to_gif}")
        return False

    # https://unix.stackexchange.com/questions/40638/how-to-do-i-convert-an-animated-gif-to-an-mp4-or-mv4-on-the-command-line
    mp4_filepath = path_to_gif + ".mp4"
    cmd = f'ffmpeg -i {path_to_gif} -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" {mp4_filepath}'

    exit_status = os.system(cmd)

    if exit_status == 0:
        return mp4_filepath
    else:
        return False
