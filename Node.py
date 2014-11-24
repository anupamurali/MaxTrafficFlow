import Road

class Node:
  """ Class for nodes in city. Node is defined by city and whether there is
  traffic light and/or toll booth"""
    def __init__(self, city, traffic_light = 0, toll_booth = 0):
      self.ID = city.city_count + 1
      self.city = city
      self.traffic_light = traffic_light
      self.toll_booth = toll_booth
      city.city_count += 1 