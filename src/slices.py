import pandas as pd


def get_columns(df):
    type_dict = {}
    for type_ in df['incident_category']:
        if type_ in type_dict:
            type_dict[type_] += 1
        else:
            type_dict[type_] = 1

    del_types = ['SPECIAL OR OTHER INCIDENT TYPE', 'FIRE, EXPLOSION',
                'SEVERE WEATHER, NATURAL DISASTER', 'HAZARDOUS CONDITION',
                'OVERPRESSURE, RUPTURE, EXPLOSION, OVERHEAT']

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

    items_to_keep = ['731 - Malfunction - due to sprinkler system activation',
                 '741 - Unintentional - sprinkler activation (no fire)',
                 '743 - Unintentional - smoke detector activation (no fire)',
                 '736 - Malfunction - due to carbon monoxide detector activation',
                 '711 - Malicious false alarm - municipal alarm system',
                 '746 - Unintentional - carbon monoxide detector activation (no CO)',
                 '740 - Unintentional - transmission of alarm, other',
                 '735 - Malfunction - due to alarm system activation',
                 '733 - Malfunction - due to smoke detector activation',
                 '730 - Malfunction - system or detector, other',
                 '700 - False alarm - false alarm or false call, other',
                 '744 - Unintentional - heat detector activation (no fire)',
                 '331 - Lock-in',
                 '742 - Unintentional - extinguishing system activation (no fire)',
                 '621 - Wrong location',
                 '714 - Malicious false alarm - monitored system',
                 '814 - Lightning strike (no fire)',
                 '611 - Dispatched & cancelled enroute',
                 '511 - Lock-out',
                 '622 - No incident found on arrival at dispatch address',

                 ]

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
