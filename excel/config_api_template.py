import pandas as pd
def check_api_and_select_template_to_compare(type_data):
    """
    Kiểm tra loại dữ liệu và chọn mẫu tương ứng để so sánh.

    Parameters:
        type_data (str): Loại dữ liệu ('course', 'room', 'timelesson', ...).

    Returns:
        pandas.DataFrame or None: DataFrame chứa mẫu tương ứng với loại dữ liệu hoặc None nếu loại dữ liệu không hợp lệ.

    Example:
        # Lấy mẫu dữ liệu cho loại 'course'
        template_df = check_api_and_select_template_to_compare('course')
    """
    template_df = None
    if type_data == 'course':
        template_df = pd.read_excel('./app/static/file/templates/course_template.xlsx')
    elif type_data == 'room':
        template_df = pd.read_excel('./app/static/file/templates/room_template.xlsx')
    elif type_data == 'timelesson':
        template_df = pd.read_excel('./app/static/file/templates/timelesson_template.xlsx')
    """ Mở rộng cho các loại dữ liệu khác """

    return template_df