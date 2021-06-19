from util import load_JSON

class Story:
    """Representation of a Muses story
    
    Methods
    -------
    has_region(path: str) -> str
        Check if story has a specific region.

    find_passage(region: str) -> str
        Find a story passage for a given region.
    """
    def __init__(self, path: str):
        # array of passages for story
        self.passages = load_JSON(path)["passages"]

    def has_region(self, region: str) -> str:
        """Check if story has a specific region
        
        Parameters
        ----------
        region : str
            The region to check is present in story
        """
        for p in self.passages:
            for tag in p["tags"]:
                if tag == region:
                    return True
        return False

    def find_passage(self, region: str) -> str:
        """Find a story passage for a given region
        
        Parameters
        ----------
        region : str 
            The region to find corresponding passage for.
        """
        for p in self.passages:
            for tag in p["tags"]:
                if tag == region:
                    return p["text"]
        return None