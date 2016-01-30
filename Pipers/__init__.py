import importlib


def autopiper(from_handler, to_handler):
    """ Sellects correct piper based on class names """
    piper_name = '{}2{}'.format(from_handler.__class__.__name__, to_handler.__class__.__name__)
    try:
        m = importlib.import_module('Pipers.{}'.format(piper_name))
        c = getattr(m, piper_name)
    except:
        raise ValueError("Piper named {} was not found!".format(piper_name))

    return c(from_handler, to_handler)
