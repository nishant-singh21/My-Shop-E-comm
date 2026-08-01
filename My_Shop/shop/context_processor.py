from .cart import Cart 

def cart(request):
    """Makes {{ cart }} available in every template, e.g.
      for a navbar item-count badge."""
    return {"cart": Cart(request)}