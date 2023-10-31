class City():
    def __init__(self, name, main_disease, connections):
        self.__name = name
        self.__main_disease = main_disease
        self.__connections = connections
        self.__disease_cubes = {"Blue":0, "Yellow":0, "Black":0, "Red":0}
        self.__research_station = False

    def get_name(self):
        return self.__name

    def get_main_disease(self):
        return self.__main_disease

    def get_connections(self):
        return self.__connections

    def get_disease_cubes(self):
        return self.__disease_cubes

    def get_research_station(self):
        return self.__research_station

    def set_disease_cubes(self, disease, n):
        self.__disease_cubes[disease] = n
        return self.__disease_cubes

    def set_research_station(self, status):
        self.__research_station = status
        return self.__research_station
    