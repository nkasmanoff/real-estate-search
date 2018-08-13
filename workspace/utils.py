
def inside_polygon(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = True
        p1x, p1y = p2x, p2y
    return inside


# In[4]:

#The API python interface
import zillow


# In[6]:

def confirm_location(zpid):
    """Identifies the lat long coords of a location and determines if it is within the right place. 
    Parameters
    ----------
    zpid : str
        The zillow listing id.
        
    Returns
    -------
    
    condo : zillow.place.Place
        The object containing basic info about the house. Will get further developed using the deep search tool. 
    """
    try:
        detail_data = api.GetZEstimate(key, zpid)
       # print("valid zpid")
        lat = float(detail_data.full_address.latitude)
        lon = float(detail_data.full_address.longitude)
        inside = inside_polygon(lat,lon,points)
       # print(inside)
        if inside:
            return detail_data  #Only if
    except:
        print("invalid zpid")
        inside = False #automatically assign as outside. 