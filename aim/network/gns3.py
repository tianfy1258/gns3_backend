"""
定义了与gns3的一系列交互
"""
from functools import wraps
import requests as r
import json


class Node:
    def __init__(self, project, compute_id, console_auto_start, console_host, console_type, first_port_name, label,
                 locked, name,
                 node_id, node_type, port_name_format, port_segment_size, ports, project_id, properties, status, symbol,
                 template_id, x, y, z, command_line=None, console=None, custom_adapters=None, height=None,
                 node_directory=None, width=None):
        if custom_adapters is None:
            custom_adapters = list()
        self.project = project
        self.compute_id = compute_id
        self.console_auto_start = console_auto_start
        self.console_host = console_host
        self.console_type = console_type
        self.first_port_name = first_port_name
        self.label = label
        self.locked = locked
        self.name = name
        self.node_id = node_id
        self.node_type = node_type
        self.port_name_format = port_name_format
        self.port_segment_size = port_segment_size
        self.ports = ports
        self.project_id = project_id
        self.properties = properties
        self.status = status
        self.symbol = symbol
        self.template_id = template_id
        self.x = x
        self.y = y
        self.z = z
        self.command_line = command_line
        self.console = console
        self.custom_adapters = custom_adapters
        self.height = height
        self.node_directory = node_directory
        self.width = width

    def __repr__(self):
        return f"<Node {self.name} {self.status}>"

    def update(self):
        node = self.project.get_node_by_id(self.node_id)
        self.__dict__.update(node.__dict__)

    def delete(self):
        self.project.server.delete(f"projects/{self.project_id}/nodes/{self.node_id}")

    def start(self):
        self.project.server.post(f"projects/{self.project_id}/nodes/{self.node_id}/start")

    def stop(self):
        self.project.server.post(f"projects/{self.project_id}/nodes/{self.node_id}/stop")

    def suspend(self):
        self.project.server.post(f"projects/{self.project_id}/nodes/{self.node_id}/suspend")


class LinkNode:
    def __init__(self, node_id, adapter_number, port_number, label=None):
        self.adapter_number = adapter_number
        self.label = label
        self.node_id = node_id
        self.port_number = port_number

    def __repr__(self):
        return f"<LinkNode {self.node_id} {self.port_number}>"

    def json(self):
        d = dict(adapter_number=self.adapter_number,
                 label=self.label,
                 node_id=self.node_id,
                 port_number=self.port_number)
        # filter out None values
        return {k: v for k, v in d.items() if v is not None}


class Link:
    def __init__(self, project, capture_compute_id, capture_file_name, capture_file_path, capturing, filters, link_id,
                 link_type, link_style,
                 nodes, project_id, suspend):
        self.project = project
        self.capture_compute_id = capture_compute_id
        self.capture_file_name = capture_file_name
        self.capture_file_path = capture_file_path
        self.capturing = capturing
        self.filters = filters
        self.link_id = link_id
        self.link_type = link_type
        self.link_style = link_style
        self.nodes = [LinkNode(**node) for node in nodes]
        self.project_id = project_id
        self.suspend = suspend

    def __repr__(self):
        return f"<Link {self.link_id} {self.link_type}>"

    def update(self):
        link = self.project.get_link_by_id(self.link_id)
        self.__dict__.update(link.__dict__)


class Project:
    def __init__(self, server, auto_close, auto_open, auto_start, drawing_grid_size, filename, grid_size, name, path,
                 project_id, scene_height, scene_width, show_grid, show_interface_labels, show_layers, snap_to_grid,
                 status, supplier, variables, zoom):
        self.server = server
        self.auto_close = auto_close
        self.auto_open = auto_open
        self.auto_start = auto_start
        self.drawing_grid_size = drawing_grid_size
        self.filename = filename
        self.grid_size = grid_size
        self.name = name
        self.path = path
        self.project_id = project_id
        self.scene_height = scene_height
        self.scene_width = scene_width
        self.show_grid = show_grid
        self.show_interface_labels = show_interface_labels
        self.show_layers = show_layers
        self.snap_to_grid = snap_to_grid
        self.status = status
        self.supplier = supplier
        self.variables = variables
        self.zoom = zoom

    def __repr__(self):
        return f"<Project {self.name} {self.status}>"

    def update(self):
        project = self.server.get_project_by_id(self.project_id)
        self.__dict__.update(project.__dict__)

    def open(self):
        self.server.post(f"projects/{self.project_id}/open")
        self.update()

    def close(self):
        self.server.post(f"projects/{self.project_id}/close")
        self.update()

    def delete(self):
        self.server.delete(f"projects/{self.project_id}")

    def export(self):
        if self.status == "opened":
            raise Exception("Please close the project before exporting")
        return self.server.get(f"projects/{self.project_id}/export")

    def get_nodes(self):
        if self.status == "closed":
            raise Exception("Project is closed")
        return [Node(project=self, **node) for node in self.server.get(f"projects/{self.project_id}/nodes")]

    def get_node_by_id(self, node_id: str):
        if self.status == "closed":
            raise Exception("Project is closed")
        return Node(project=self, **self.server.get(f"projects/{self.project_id}/nodes/{node_id}"))

    def get_node_by_name(self, name: str):
        nodes = self.get_nodes()
        for node in nodes:
            if node.name == name:
                return node
        raise Exception(f"Node {name} not found")

    def create_node(self, node_type: str, name: str, compute_id: str = "vm", **kwargs):
        response = self.server.post(f"projects/{self.project_id}/nodes",
                                    node_type=node_type, name=name, compute_id=compute_id, **kwargs)
        node_id = response["node_id"]
        return self.get_node_by_id(node_id)

    def get_links(self):
        if self.status == "closed":
            raise Exception("Project is closed")
        return [Link(project=self, **link) for link in self.server.get(f"projects/{self.project_id}/links")]

    def get_link_by_id(self, link_id: str):
        if self.status == "closed":
            raise Exception("Project is closed")
        return Link(project=self, **self.server.get(f"projects/{self.project_id}/links/{link_id}"))

    def create_link(self, source_link_node: LinkNode,
                    dest_link_node: LinkNode,
                    ):
        if self.status == "closed":
            raise Exception("Project is closed")
        response = self.server.post(f"projects/{self.project_id}/links",
                                    nodes=[source_link_node.json(), dest_link_node.json()])
        link_id = response["link_id"]
        return self.get_link_by_id(link_id)


class Server:
    def __init__(self,
                 host,
                 port, ):
        self.base_url = f"http://{host}:{port}/v2"

    def get(self, url: str):
        response = r.get(f"{self.base_url}/{url}")
        if response.status_code >= 400:
            raise Exception(f"GET {url} failed with {response.status_code}"
                            f" {response.text}")
        try:
            return response.json()
        except Exception:
            return {"data": response.content.decode("utf-8")}

    def post(self, url: str, **kwargs):
        response = r.post(f"{self.base_url}/{url}", json=kwargs)
        if response.status_code >= 400:
            raise Exception(f"POST {url} failed with {response.status_code}"
                            f" {response.text}")
        try:
            res = response.json()
            return res
        except Exception:
            return {"data": response.content.decode("utf-8")}

    def delete(self, url: str):
        response = r.delete(f"{self.base_url}/{url}")
        if response.status_code >= 400:
            raise Exception(f"DELETE {url} failed with {response.status_code}"
                            f" {response.text}")
        try:
            return response.json()
        except Exception:
            return {"data": response.content.decode("utf-8")}

    def get_version(self):
        return self.get("version")

    def create_project(self, name: str, **kwargs):
        response = self.post("projects", name=name, **kwargs)
        pid = response["project_id"]
        return self.get_project_by_id(pid)

    def get_project_by_id(self, project_id: str):
        response = self.get(f"projects/{project_id}")
        return Project(server=self, **response)

    def get_project_by_name(self, name: str):
        projects = self.get_projects()
        for project in projects:
            if project.name == name:
                return project
        raise Exception(f"Project {name} not found")

    def get_projects(self):
        return [Project(server=self, **project) for project in self.get("projects")]
