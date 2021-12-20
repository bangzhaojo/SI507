class County:
    def __init__(self, fip=None, name=None, state=None, population=None, vac_rate=None, case_rate=None,
                 death_rate=None, ratio_island=None, ratio_white=None, ratio_black=None, ratio_asian=None,
                 ratio_native=None, ratio_other=None, ratio_poverty=None, parent=None, json=None):
        if json is None:
            self.fip = fip
            self.name = name
            self.state = state
            self.population = population
            self.vac_rate = vac_rate
            self.case_rate = case_rate
            self.death_rate = death_rate
            self.ratio_island = ratio_island
            self.ratio_white = ratio_white
            self.ratio_black = ratio_black
            self.ratio_asian = ratio_asian
            self.ratio_native = ratio_native
            self.ratio_other = ratio_other
            self.ratio_poverty = ratio_poverty
            self.children = []
            self.parent = parent
            self.size = None
            self.minority = None
        else:
            self.fip = json["fip"]
            self.name = json["name"]
            self.state = json["state"]
            self.population = json["population"]
            try:
                self.vac_rate = json["vacRate"]
            except:
                self.vac_rate = None
            self.case_rate = json["caseRate"]
            self.death_rate = json["deathRate"]
            self.ratio_island = json["ratioIsland"]
            self.ratio_white = json["ratioWhite"]
            self.ratio_black = json["ratioBlack"]
            self.ratio_asian = json["ratioAsian"]
            self.ratio_native = json["ratioNative"]
            self.ratio_other = json["ratioOther"]
            self.ratio_poverty = json["ratioPoverty"]
            self.children = []
            self.parent = parent
            self.size = None
            self.minority = None


    def getid(self):
        return self.fip

    def getname(self):
        return self.name

    def add_child(self, county):
        self.children.append(county)

    def add_parent(self, county):
        self.parent = county


class Tree:
    def __init__(self, root):
        self.root = root

    def getroot(self):
        return self.root
