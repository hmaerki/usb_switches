import pathlib

TAG_IMAGES_START = '--- images start ---'
TAG_IMAGES_END = '--- images end ---'


for readme in pathlib.Path(__file__).parent.glob('*/readme.md'):
    images = [img for img in readme.parent.glob('*') if img.suffix.lower() in ('.jpeg', '.jpg', '.png')]
    print(readme, images)
    readme_text = readme.read_text()



    pos_start = readme_text.find(TAG_IMAGES_START)
    text = readme_text
    if pos_start >= 0:
        text = readme_text[0:pos_start]

    text += TAG_IMAGES_START
    text += '\n'
    text += '\n'.join([f'![]({img.name})' for img in sorted(images)])
    text += '\n'
    text += TAG_IMAGES_END

    pos_end = readme_text.find(TAG_IMAGES_END)
    end_text = ''
    if pos_end >= 0:
        text += readme_text[pos_end+len(TAG_IMAGES_END):]
    
    readme.write_text(text)
