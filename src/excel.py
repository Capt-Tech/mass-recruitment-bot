import constants


def validate_interview_file(path):
    is_interview_path = path == constants.get_interview_path()
    return True
