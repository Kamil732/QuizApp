VALID_IMAGE_EXTENSIONS = (
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
)

def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    return any([url.endswith(i) for i in extension_list])