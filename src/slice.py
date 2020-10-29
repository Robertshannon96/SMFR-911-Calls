from pyproj import Proj, transform


def get_columns(df):
    type_dict = {}
    for type_ in df['incident_category']:
        if type_ in type_dict:
            type_dict[type_] += 1
        else:
            type_dict[type_] = 1

    del_types = ['SPECIAL OR OTHER INCIDENT TYPE', 'FIRE, EXPLOSION', 'SEVERE WEATHER, NATURAL DISASTER',
                 'HAZARDOUS CONDITION', 'OVERPRESSURE, RUPTURE, EXPLOSION, OVERHEAT']

    for types in del_types:
        del type_dict[types]

    return type_dict


def get_types(df):
    full_inc_type = {}

    for inc in df['incident_type']:
        if inc in full_inc_type:
            full_inc_type[inc] += 1
        else:
            full_inc_type[inc] = 1

    items_to_keep = ['511 - Lock-out', '743 - Unintentional - smoke detector activation (no fire)',
                     '733 - Malfunction - due to smoke detector activation']

    inc_type = {x: full_inc_type[x] for x in items_to_keep}

    return inc_type


def get_night_calls(df):
    night_df = df[(df['hour'] >= 22) | (df['hour'] <= 5)]
    night_lock_outs = night_df[night_df['incident_type'] == '511 - Lock-out']

    return night_lock_outs


def get_place(night_lock_outs):
    property_use = {}

    for place in night_lock_outs['property_use']:
        if place in property_use:
            property_use[place] += 1
        else:
            property_use[place] = 1

    return property_use


def get_incidents(df):
    incidents = df[(df['incident_type'] == '511 - Lock-out') | (df['incident_type'] ==
                 '743 - Unintentional - smoke detector activation (no fire)') |
                (df['incident_type'] == '733 - Malfunction - due to smoke detector activation')]

    return incidents


def lockout(df, night_df):
    lock_outs = df[df['incident_type'] == '511 - Lock-out']
    night_lock_out = night_df[night_df['incident_type'] == '511 - Lock-out']

    return lock_outs, night_lock_out


def get_unintentional(df, night_df):
    unintentional = df[df['incident_type'] == '743 - Unintentional - smoke detector activation (no fire)']
    unintentional_night = night_df[
        night_df['incident_type'] == '743 - Unintentional - smoke detector activation (no fire)']

    return unintentional, unintentional_night


def get_malfunction(df, night_df):
    malfunction = df[df['incident_type'] == '733 - Malfunction - due to smoke detector activation']
    malfunction_night = night_df[
            night_df['incident_type'] == '733 - Malfunction - due to smoke detector activation']

    return malfunction, malfunction_night

