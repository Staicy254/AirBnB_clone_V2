#!/usr/bin/python3
"""Console Module"""
import cmd
import sys
import re
import os
from datetime import datetime
import uuid
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains functionality for HBNB console"""

    prompt = '(hbnb) ' if sys.stdin.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        if not all(char in line for char in ['.', '(', ')']):
            return line

        try:
            class_name, dot_cmd, params = re.split(r'[.(]', line.strip(), maxsplit=2)
            args = re.findall(r'(\w+)=([^,)]+)', params)

            args = [(key, eval(val)) if val.startswith('"') else (key, val) for key, val in args]

            line = f"{dot_cmd} {class_name} "
            if args:
                line += ' '.join(f'{key} {val}' for key, val in args)

        except Exception as e:
            pass
        finally:
            return line

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        sys.exit(0)

    def do_create(self, args):
        """Create an object of any class"""
        class_name, *params = args.split(' ')
        obj_kwargs = {}

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        for param in params:
            key, val = param.split('=')
            obj_kwargs[key] = self.types.get(key, str)(val)

        new_instance = self.classes[class_name](**obj_kwargs)
        new_instance.save()
        print(new_instance.id)

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            class_name = args.split(' ')[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            print_list = [str(v) for k, v in storage.all().items() if k.split('.')[0] == class_name]
        else:
            print_list = [str(v) for v in storage.all().values()]

        print(print_list)

    def do_count(self, args):
        """Count current number of class instances"""
        class_name = args.split(' ')[0]
        count = sum(1 for k in storage.all() if k.split('.')[0] == class_name)
        print(count)

    def do_update(self, args):
        """Updates a certain object with new info"""
        class_name, obj_id, *updates = args.split(' ')

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if not obj_id:
            print("** instance id missing **")
            return

        key = f"{class_name}.{obj_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        instance = storage.all()[key]
        for update in updates:
            attr, value = update.split('=')
            setattr(instance, attr, self.types.get(attr, str)(value))
        storage.save()

    def postloop(self):
        """Prints if isatty = false"""
        if not sys.stdin.isatty():
            print('(hbnb) ', end='')


if __name__ == "__main__":
    HBNBCommand().cmdloop()

