from app.auth.auth import requires_auth
from app.models.task import Task
from app.repositories.task_manager import TaskManager
from flask import Blueprint,_request_ctx_stack
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
import argparse

task_manager = TaskManager()


def str2bool(v):
    
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

task_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'done': fields.Boolean
}

resource_fields_filter = { 'count': fields.Integer, 'tasks':fields.List(fields.Nested(task_fields))}

   
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)
parser.add_argument('done', type=str2bool)

parser_list = reqparse.RequestParser()
parser_list.add_argument('done', type=str2bool, location='args')

parser_filter = reqparse.RequestParser()
parser_filter.add_argument('term', type=str, default=None)
parser_filter.add_argument('page', type=int)
parser_filter.add_argument('sort', type=str)
parser_filter.add_argument('order', type=str)

class TaskListResource(Resource):
        @marshal_with(task_fields)
        @requires_auth
        def get(self):
            args = parser_list.parse_args()
            
            return task_manager.list_all_tasks(args.done, _request_ctx_stack.top.current_user['sub'])

        @marshal_with(task_fields)
        @requires_auth
        def post(self):
            args = parser.parse_args()
            
            task = task_manager.new_task(args.name, args.description, args.done, _request_ctx_stack.top.current_user['sub'])

            return {"id":task.id, "name":task.name, "description":task.description, "done":task.done}, 200            


class TaskFilterResource(Resource):
        @marshal_with(resource_fields_filter)
        @requires_auth
        def get(self):
            args = parser_filter.parse_args()
            return task_manager.filter_tasks(args.term, args.page, args.sort, args.order, _request_ctx_stack.top.current_user['sub'])            
        
        
class TaskResource(Resource):
        #@marshal_with(task_fields)
        #@requires_auth
        #def get(self, task_id):
        #    task = task_manager.get_task_by_id(task_id)
        #     
        #    return {"id": task.id, "name": task.name, "description": task.description, "done": task.done}

        @marshal_with(task_fields)
        @requires_auth
        def put(self, task_id):
            args = parser.parse_args()

            task = task_manager.edit_task(task_id, args.name, args.description, args.done, _request_ctx_stack.top.current_user['sub'])

            return {"id":task.id, "name":task.name, "description":task.description, "done":task.done}, 200            

        @requires_auth
        def delete(self, task_id):
            task_manager.remove_task(task_id, _request_ctx_stack.top.current_user['sub'])

            return {"message": "Task was succesfully removed"}, 200
            

    
tasks_bp = Blueprint('tasks', __name__)
api_tasks = Api(tasks_bp)


api_tasks.add_resource(TaskListResource, '/')
api_tasks.add_resource(TaskFilterResource, '/filter')
api_tasks.add_resource(TaskResource, '/task/<int:task_id>')