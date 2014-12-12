SOURCE_COLOR = (0,255,0)
SINK_COLOR = (255,0,255)
NODE_COLOR = (0,0,255)
ROAD_COLOR = (255,0,0)
ALL_DIRECTIONS =  [(-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1,-1), (1,0), (1,1)]

from PIL import Image, ImageFont, ImageDraw
import sys
import json
import random

def load_image(imgfile):
    im = Image.open(imgfile)
    width, height = im.size
    rgb_im = im.convert('RGB')
    pixelmap = [[rgb_im.getpixel((x, y)) for y in xrange(height)] for x in xrange(width)]
    return pixelmap, im

def find_node_with_color(pixels, color):
    width = len(pixels)
    height = len(pixels[0])
    for x in xrange(width):
        for y in xrange(height):
            if pixels[x][y] == color:
                return (x,y)
    return None

def in_bounding_box(pos, boundingbox):
    left, right, top, bottom = boundingbox
    x,y = pos
    if x >= left and x <= right and y >= top and y <= bottom:
        return True
    return False

def remove_duplicates(pixels, adj_nodes):
    """
    Removes multiple references to the same node (i.e. adj_nodes contains multiple pixels from the same node)
    """
    boundaries = []
    unique_nodes = []
    for pos, dist in adj_nodes:
        # Make sure we haven't seen this node before
        isDuplicate = False
        for bbox in boundaries:
            if in_bounding_box(pos, bbox):
                isDuplicate = True
                break
        if not isDuplicate:
            components = get_node_component_pixels(pixels, pos)
            boundary = get_bounding_box(components)
            boundaries.append(boundary)
            unique_nodes.append( (pos, dist) )
    return unique_nodes


def find_adjacent_nodes(pixels, startpos, boundingbox):
    """
    Returns a list of adjacent nodes. Only gives 1 coordinate for each adjacent node.
    """
    Q = [startpos]
    visited = []
    adj_nodes = []
    orig_color = pixels[startpos[0]][startpos[1]]
    parent = {startpos: None}
    while Q:
        x, y = Q.pop(0)
        from_road = (pixels[x][y] == ROAD_COLOR)
        for offx, offy in ALL_DIRECTIONS:
            newx = x + offx
            newy = y + offy
            # If coming from a road, check for node-colored or sink-colored pixels that aren't from original node
            isNodeColorPixel = pixels[newx][newy] == SINK_COLOR or pixels[newx][newy] == NODE_COLOR
            foundOtherNode = from_road and (isNodeColorPixel and not in_bounding_box((newx, newy), boundingbox)) and ((newx, newy) not in visited)
            if foundOtherNode:
                # Get the distance to this node along the road in pixels
                p = (x,y)
                dist = 0
                while p:
                    # Stop increasing distance if we get back to the original node
                    if pixels[p[0]][p[1]] != ROAD_COLOR:
                        break
                    p = parent[p]
                    dist += 1
                # Add this node to our list of adjacent nodes
                adj_nodes.append(((newx,newy), dist))
                visited.append( (newx, newy) )
            # Otherwise, look for other pixels in this node or follow a road
            if (pixels[newx][newy] == orig_color or pixels[newx][newy] == ROAD_COLOR) and (newx, newy) not in visited:
                Q.append( (newx, newy) )
                visited.append( (newx, newy) )
                parent[(newx, newy)] = (x,y)

    adj_nodes = remove_duplicates(pixels, adj_nodes)
    return adj_nodes


def get_node_component_pixels(pixels, startpos):
    """
    Returns a list of all pixels of the same color that border this pixel (incl. diagonal)
    """
    origx, origy = startpos
    color = pixels[origx][origy]
    Q = [startpos]
    visited = []
    while Q:
        x, y = Q.pop(0)
        for offx, offy in ALL_DIRECTIONS:
            newx = x + offx
            newy = y + offy
            if pixels[newx][newy] == color and (newx, newy) not in visited:
                Q.append( (newx, newy) )
                visited.append( (newx, newy) )
    return visited

def get_bounding_box(component_pixels):
    """
    Returns the leftmost, rightmost, topmost and bottommost pixels for a given list of pixels
    """
    pos = component_pixels[0]
    left = pos[0]
    right = pos[0]
    top = pos[1]
    bottom = pos[1]
    for x, y in component_pixels:
        left = min(x,left)
        right = max(x,right)
        top = min(y,top)
        bottom = max(y,bottom)
    return (left, right, top, bottom)



def get_node_id(all_nodes, pos):
    for id, data in all_nodes.iteritems():
        boundbox = data['boundingbox']
        if in_bounding_box(pos, boundbox):
            return id
    return None

def add_node(all_nodes, id, pos, boundbox):
    all_nodes[id] = {"pos": pos, "boundingbox": boundbox, "edges": []}
    return all_nodes

def add_edge(all_nodes, id1, id2, dist):
    all_nodes[id1]["edges"].append((id2,dist))
    return all_nodes

def get_next_id():
    x = 1
    while(True):
        yield str(x)
        x += 1

def export_to_json(all_nodes, filename):
    json_data = json.dumps(all_nodes)
    with open(filename, "w") as f:
        f.write(json_data)

def export_labeled_image(all_nodes, inimgfile, outimgfile):
    img = Image.open(inimgfile)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 32)
    for id, data in all_nodes.iteritems():
        pos = data["pos"]
        draw.text(pos,id,(0,0,0),font=font)
    img.save(outimgfile)

def export_colored_image(all_nodes, colorings, inimgfile, outimgfile):
    pixels, im = load_image(inimgfile)
    pixdata = im.load()
    for id, color in colorings:
        surround = get_node_component_pixels(pixels, all_nodes[id]["pos"])
        for x,y in surround:
            if random.random()<0.60:
                pixdata[x,y] = color
    im.save(outimgfile)


def import_from_json(filename):
    with open(filename, "r") as f:
        all_nodes = json.load(f)
    return all_nodes

def convert_image_to_citydata(image_file, outfile, outimgfile):
    next_id_generator = get_next_id()

    pixels, _ = load_image(image_file)

    # Create container for all nodes we've saved
    all_nodes = {}
    already_processed = set()

    # Add source and sink
    src_id = "s"
    sink_id = "t"
    src_pos = find_node_with_color(pixels, SOURCE_COLOR)
    sink_pos = find_node_with_color(pixels, SINK_COLOR)
    src_boundbox = get_bounding_box(get_node_component_pixels(pixels, src_pos))
    sink_boundbox = get_bounding_box(get_node_component_pixels(pixels, sink_pos))
    all_nodes = add_node(all_nodes, src_id, src_pos, src_boundbox)
    all_nodes = add_node(all_nodes, sink_id, sink_pos, sink_boundbox)
    # Pretend we've already processed the sink so we don't add any edges from it
    already_processed.add(sink_id)
    # Initialize the queue with the source only
    Q = [src_id]

    # Explore until we've exhausted the city graph
    while Q:
        pos_id = Q.pop(0)
        pos = all_nodes[pos_id]["pos"]
        pos_pixels = get_node_component_pixels(pixels, pos)
        pos_boundbox = get_bounding_box(pos_pixels)
        adj_nodes = find_adjacent_nodes(pixels, pos, pos_boundbox)
        for adj_pos, adj_dist in adj_nodes:
            adj_id = get_node_id(all_nodes, adj_pos)
            # If node doesn't exist, calculate its bounding box and add it.
            if not adj_id:
                adj_id = next_id_generator.next()
                boundbox = get_bounding_box(get_node_component_pixels(pixels, adj_pos))
                all_nodes = add_node(all_nodes,adj_id,adj_pos,boundbox)
            # If it has not been processed, add it to the Queue
            if adj_id not in already_processed:
                already_processed.add(adj_id)
                Q.append(adj_id)
            # Add an edge to this node
            all_nodes = add_edge(all_nodes, pos_id, adj_id, adj_dist)

    for id, data in all_nodes.iteritems():
        print "INFO FOR NODE", id
        print "    EDGES:"
        for dest, dist in data["edges"]:
            print "        ",dest, "(",dist,")"

    export_to_json(all_nodes, outfile)
    export_labeled_image(all_nodes, image_file, outimgfile)
    return all_nodes

if __name__ == "__main__":
    image_file = sys.argv[1]
    name, ext = image_file.split('.')
    outfile = name + ".json"
    outimgfile = name + "_labeled." + ext
    convert_image_to_citydata(image_file, outfile, outimgfile)
