import todo_pb2_grpc
import todo_pb2
import grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.TodoStub(channel)
        print("1. Create Todo")
        print("2. Read Todos")
        rpc_call = input("which rpc would you like to call?\n")

        if rpc_call == "1":
            text = input("Enter the text for your todo item: ")
            request = todo_pb2.TodoItem(id=-1, text=text)
            response = stub.createTodo(request)
            print("Created Todo Item\n %d: %s" % (response.id, response.text))
        elif rpc_call == "2":
            read_response = stub.readTodos(todo_pb2.void())
            print("\nTodo List:")
            for item in read_response.items:
                print("%d: %s" % (item.id, item.text))
        else:
            print("Invalid selection")

if __name__ == "__main__":
    run()