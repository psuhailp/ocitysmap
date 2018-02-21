# -*- coding: utf-8 -*-

import json, re

def umap_preprocess(umap_file):
    umap_defaults = {
        'color'      :   'blue',
        'opacity'    :      0.5,
        'fillColor'  :   'blue',
        'fillOpacity':      0.2,
        'weight'     :        3,
        'fill'       :    'yes',
        'stroke'     :    'yes',
        'name'       :       '',
        'iconClass'  : 'Square',
        'iconUrl'    : 'circle'
    }

    marker_offsets = {
        'Square': -18,
        'Drop'  : -18,
        'Circle': 0,
        'Ball'  : -16
    }

    fp = open(umap_file, 'r')

    umap = json.load(fp)

    for prop in ['color', 'opacity', 'fillColor', 'fillOpacity', 'weight']:
        if prop in umap['properties']:
            umap_defaults[prop] = umap['properties'][prop]

    layers = umap['layers']

    new_features = []

    for layer in layers:
        for feature in layer['features']:
            new_props = {}
            for prop in ['name', 'color', 'opacity', 'fillColor', 'fillOpacity', 'weight', 'fill', 'stroke']:
                new_props[prop] = umap_defaults[prop]
                try:
                    if prop in feature['properties']:
                        new_props[prop] = feature['properties'][prop]
                    elif prop in feature['properties']['_storage_options']:
                        new_props[prop] = feature['properties']['_storage_options'][prop]
                except:
                    pass

            if feature['geometry']['type'] == 'Point':
                try:
                    iconClass = feature['properties']['_storage_options']['iconClass']
                except:
                    iconClass = umap_defaults['iconClass']

                try:
                    iconUrl = feature['properties']['_storage_options']['iconUrl']
                except:
                    iconUrl = umap_defaults['iconUrl']

                new_props['iconClass'] = iconClass

                if iconClass == 'Square' or iconClass == 'Drop':
                    m = re.match(r'/uploads/pictogram/(.*)-24.*png', iconUrl)
                    if m:
                        new_props['iconUrl'] = m.group(1)
                    else:
                        new_props['iconUrl'] = iconUrl

                try:
                    new_props['offset'] = marker_offsets[iconClass]
                except:
                    pass

            new_props['weight'] = float(new_props['weight']) / 4
                        
            new_features.append({
                'type'       : 'Feature', 
                'properties' : new_props, 
                'geometry'   : feature['geometry']
                })

    new_umap = {
        'type'     : 'FeatureCollection', 
        'features' : new_features
    }

    return json.dumps(new_umap, indent=2)