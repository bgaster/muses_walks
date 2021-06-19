from geopy import distance

from util import load_JSON

class GeoFences:
    """Representation of Geo regions for story

    Attributes
    ----------
    features: str 
        Dict represention of GeoJSON features
    in_regions: set(str)
        A set containing the currently in region tags

    Methods
    -------
    move(loc: (float, float)) -> (set(str), set(str), set(str))
        Check if story has a specific region.
    """
    def __init__(self, path):
        # array of features that represent a geo fence region
        self.features = load_JSON(path)["features"]
        # set containing the names of regions we are in
        self.in_regions = set()

    # Returns a tuple containing Geo regions that we left, entered, or remained in
    def move(self, loc):

        in_regions = set()

        for f in self.features:
            p = f["properties"]
            g = f["geometry"]
            c = g["coordinates"]
            # TODO: the lat/long are around the wrong way in the GeoJSON outputted by the webapp. Need to 
            #       fix the webapp and the update here.
            l = (round(c[1],6), round(c[0],6))
            #loc = (round(loc[1],6), round(loc[0],6))
            r = p["radius"]

            # print(p["name"])
            # print("CLat: {0:.6f} degrees".format(l[0]))
            # print("CLong: {0:.6f} degrees".format(l[1]))

            # are we inside geo fence?
            dist = distance.distance(l, loc).km * 1000
            # print("Dist: {0:.6f} mts".format(dist))
            if (dist) < r:
                n = p["name"]
                in_regions.add(n)

        # calculate Geo regions that we left, entered, or remained in
        left_regions     = self.in_regions - in_regions
        entered_regions  = in_regions - self.in_regions
        remained_regions = self.in_regions.intersection(in_regions)

        # update the current regions we are in
        self.in_regions  = in_regions

        # finally return the region changes
        return (left_regions, entered_regions, remained_regions)
