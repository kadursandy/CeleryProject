def uuid(outer_func):
    import uuid

    def wrapper(*args, **kwargs):
        n_uuid = uuid.uuid4()
        return outer_func(n_uuid, *args, **kwargs)
    return wrapper


@uuid
def business_logic(n_uuid=None):
    print(f'Inside the func UUID i = ', n_uuid)
    return n_uuid


if __name__ == '__main__':
    # n_uuid = None
    # should access uuid here
    print(business_logic())
