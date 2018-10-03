from core.sockets.messages import Message
from core.sockets.client import SocketClient

sc = SocketClient()

#print(sc.check_connection())

request = (
    Message()
    .add_entry('type', 'request')
    .add_entry('content', 'ciao ciao')
    .add_entry('exec_path', '/opt/sledge/tasks/remotedummy')
    .add_entry('parameters', 'verbose')
    .to_bytes(4096)
)

sc = SocketClient()

#print(sc.check_connection)

response = sc.send_request(request)

print(response)
