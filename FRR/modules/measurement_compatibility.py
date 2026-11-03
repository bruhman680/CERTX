"""Optional descriptive receipt; compatibility does not establish causal truth.

Caller supplies accepted (class, measurement-setting) pairs and independently
allowed measurement settings. This function does not fit/calibrate/test anything.
"""
def describe_compatibility(accepted_pairs, allowed_measurements, declared_classes):
    order=tuple(declared_classes)
    if not order or len(set(order))!=len(order):raise ValueError('Require distinct declared classes')
    accepted=set(tuple(p) for p in accepted_pairs);allowed=set(allowed_measurements)
    if any(len(p)!=2 or p[0] not in order for p in accepted):raise ValueError('Unknown class or malformed pair')
    retained=accepted & {(c,m) for c in order for m in allowed}
    classes=tuple(c for c in order if any(p[0]==c for p in retained))
    if not allowed:status='CALIBRATION_GRID_EMPTY'
    elif not retained:status='NO_COMPATIBLE_PAIR'
    elif len(classes)>1:status='AMBIGUOUS_CLASSES'
    else:status='COMPATIBLE_CLASS'
    return {'status':status,'compatible_classes':list(classes),'retained_pairs':sorted(retained,key=lambda p:(order.index(p[0]),repr(p[1]))),'allowed_measurement_count':len(allowed),'accepted_pairs_before_calibration':len(accepted),'claim_scope':'compatibility within supplied class/measurement candidates; no causal identification'}
