from concurrent import futures 
import logging
import grpc
import todo_pb2
import todo_pb2_grpc

# Store todos in memory
todos = []
next_id = 1

class TodoServicer(todo_pb2_grpc.TodoServicer):

    def createTodo(self, request, context):
        logging.info(f"Created Todo: {request}")
        global next_id

        # Assign a new ID if -1 is passed
        todo_id = next_id if request.id == -1 else request.id
        next_id += 1

        #create new TodoItem
        new_todo = todo_pb2.TodoItem(id=todo_id, text=request.text)
        todos.append(new_todo)
        return new_todo

    
    def readTodos(self, request, context):
        logging.info("Reading Todos")
        return todo_pb2.TodoItems(items=todos)
    
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServicer_to_server(TodoServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    server()