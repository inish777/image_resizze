def check_size_for_image(width, height, size):
    max_width, max_height = size.split('x')
    if int(width) <= int(max_width) and int(height) < int(max_height):
        return True
    return False

def check_content_type_by_response(response_headers):
    if response_headers.get('content-type').startswith('image'):
        return True
    return False