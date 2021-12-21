from operator import indexOf
from sqlalchemy import or_
from sqlalchemy.orm.util import aliased
from app.models.task import Task
from flask_restful import abort
from app import db, get_config
from app.models.user import User


class TaskManager:

    def new_task(self, name, description, done, user_name):
        existing_user = User.query.filter(User.name == user_name).first()

        if(existing_user is None):
            existing_user = User(name=user_name)
            db.session.add(existing_user)

        task = Task(name=name, description=description, done=done, user=existing_user)
        db.session.add(task)
        db.session.commit()

        return task

    def get_task_by_id(self, id, user_name):
        task = Task.query.filter(Task.id == id).join(Task.user).filter_by(name=user_name).first()

        if(not task):
            abort(404, message=f"Task {id} doesn't exist")
        
        return task
            
        
    def edit_task(self, id, name, description, done, user_name):
        task = self.get_task_by_id(id, user_name)

        task.name = name
        task.description = description
        task.done = done
        
        db.session.commit()
        
        return task

    def remove_task(self, id, user_name):
        task = self.get_task_by_id(id, user_name)

        db.session.delete(task)
        db.session.commit()

    def list_all_tasks(self, done, user_name):
        if(done is None):
            return Task.query.join(Task.user).filter_by(name=user_name).all()    
        return Task.query.join(Task.user).filter_by(name=user_name).filter(Task.done == done).all()

    def filter_tasks(self, term, page, sort, order, user_name):
        offset = (page-1) * get_config().TASK_PAGE_SIZE
        term = "" if term is None else term
        sort_field = {"name": Task.name, "description":Task.description}[sort]
        sort_field_with_order_by = {"asc": sort_field.asc(), "desc": sort_field.desc()}[order]
        filter_to_use = or_(Task.name.like(f'%{term}%'), Task.description.like(f'%{term}%'))
        count_tasks = Task.query.filter(filter_to_use).count()
        records = Task.query.join(Task.user).filter_by(name=user_name).filter(filter_to_use) \
                    .order_by(sort_field_with_order_by) \
                    .offset(offset).limit(get_config().TASK_PAGE_SIZE).all()
        return {"count":count_tasks, "tasks":records}
