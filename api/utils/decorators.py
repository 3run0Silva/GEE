from functools import wraps
from flask import jsonify

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from execptions.NotFoundException import NotFoundException

# Status code handling (ERRORS)
def error_handler(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    try:
      return f(*args, **kwargs)
    except NotFoundException as e:
      return jsonify({'error': str(e)}), 404
  return decorated_function