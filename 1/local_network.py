class Server:
    ip_counter = 1

    def __init__(self):
        self.ip = Server.ip_counter
        Server.ip_counter += 1
        self.buffer = []
        self.router = None

    def send_data(self, data_str, dest_ip):
        if self.router:
            data = Data(data_str, dest_ip)
            self.router.buffer.append(data)
        else:
            raise ValueError("Error: Server is not linked to a router")

    def get_data(self):
        data = self.buffer.copy()
        self.buffer.clear()
        return data


class Router:
    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, server):
        self.servers[server.ip] = server
        server.router = self

    def unlink(self, server):
        if server.ip in self.servers:
            del self.servers[server.ip]
            server.router = None

    def send_data(self):
        for data in self.buffer:
            if data.ip in self.servers:
                self.servers[data.ip].buffer.append(data)
        self.buffer.clear()


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


sv1 = Server()
sv2 = Server()
router = Router()

router.link(sv1)
router.link(sv2)

sv1.send_data("Test", sv2.ip)
sv2.send_data("Test2", sv1.ip)

router.send_data()

received_data = sv1.get_data()
for data in received_data:
    print(f"IP {sv1.ip} received: {data.data}")

received_data = sv2.get_data()
for data in received_data:
    print(f"IP {sv2.ip} received: {data.data}")
