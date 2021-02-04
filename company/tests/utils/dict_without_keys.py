from copy import deepcopy


def dict_without_keys(data_: dict, keys: list):
    """
    Example:
        from dictdiffer import diff

        assert list(diff(
        dict_without_keys(listing.to_dict(), ['_id', '_cls', 'created_date', 'updated_date', 'rooms[].id', 'photos']),
        dict_without_keys(normal_listing_dict, ['photos'])
    )) == []
    """
    data = deepcopy(data_)
    flat_keys = []  # keys like 'created_date'
    inner_list_keys = {}  # keys like 'rooms[].id'

    for key in keys:
        if "[]." in key:
            inner_list_key, key_to_cut_out = key.split("[].")  # ('rooms', 'id')

            if inner_list_key not in inner_list_keys:
                inner_list_keys[inner_list_key] = []

            inner_list_keys[inner_list_key].append(key_to_cut_out)
        else:
            flat_keys.append(key)

    # filter out flat keys
    data = {k: v for k, v in data.items() if k not in flat_keys}

    # filter out inner_list_keys
    for inner_list_key, keys_to_cut_out in inner_list_keys.items():
        # if data really has non-empty inner list of dicts named 'rooms'
        if (
            (inner_list_key in data)
            and (type(data[inner_list_key]) == list)
            and (len(data[inner_list_key]) > 0)
            and (type(data[inner_list_key][0]) == dict)
        ):
            # iterate through rooms
            for i in range(len(data[inner_list_key])):
                # cut out 'id' from room i
                data[inner_list_key][i] = {
                    k: v
                    for k, v in data[inner_list_key][i].items()
                    if k not in keys_to_cut_out
                }

    return data
